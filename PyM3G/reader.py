"""
Module for reading JSR 184 m3g files
"""
from io import BytesIO
from struct import unpack, pack
import zlib

import logging
from rich.logging import RichHandler

from .util import M3GStatus

from .objects.animation import AnimationController, AnimationTrack, KeyframeSequence
from .objects.appearance import (
    Appearance,
    CompositingMode,
    Fog,
    Material,
    PolygonMode,
    Texture2D,
)
from .objects.misc import Background, ExternalReference, Header, Image2D
from .objects.nodes import Camera, Group, Light, Mesh, Sprite
from .objects.nodes_extra import MorphingMesh, SkinnedMesh, World
from .objects.vertex import TriangleStripArray, VertexArray, VertexBuffer

_M3G_SIG = b"\xAB\x4A\x53\x52\x31\x38\x34\xBB\x0D\x0A\x1A\x0A"

LOG_LEVEL = "WARNING"

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("m3g")
log.setLevel(logging.getLevelName(LOG_LEVEL))


class M3GReader:
    """
    Reader for JSR 184 M3G data files
    """

    _type2class = {
        0: Header,
        1: AnimationController,
        2: AnimationTrack,
        3: Appearance,
        4: Background,
        5: Camera,
        6: CompositingMode,
        7: Fog,
        8: PolygonMode,
        9: Group,
        10: Image2D,
        11: TriangleStripArray,
        12: Light,
        13: Material,
        14: Mesh,
        15: MorphingMesh,
        16: SkinnedMesh,
        17: Texture2D,
        18: Sprite,
        19: KeyframeSequence,
        20: VertexArray,
        21: VertexBuffer,
        22: World,
        255: ExternalReference,
    }

    def __init__(self, path):
        self.status = M3GStatus.FAILED
        self.objects = []
        self.file = open(path, "rb")
        if not self.file:
            log.error("Could not open file %s", path)
            return
        if not self.verify_signature():
            log.error("Invalid M3G file %s", path)
            self.file.close()
            return
        self.read_sections()
        self.file.close()
        self.status = M3GStatus.SUCCESS

    def verify_signature(self):
        """Verify header bytes to make sure this is a valid m3g file"""
        if self.file.read(12) == _M3G_SIG:
            return True
        return False

    def parse_object(self, objtype, data):
        """Parse an object out of a binary data chunk"""
        rdr = BytesIO(data)
        if objtype in self._type2class:
            obj = self._type2class.get(objtype)()
        else:
            obj = None
            log.error("Invalid object type(%d) found", objtype)
            rdr.close()
            return None
        log.info(
            "Found [bold cyan]%s[/] object",
            obj.__class__.__name__,
            extra={"markup": True},
        )
        obj.read(rdr)

        bytes_unread = len(rdr.read())
        if obj is None and bytes_unread > 0:
            log.warning("%d bytes left unread", bytes_unread)
        rdr.close()
        return obj

    def read_objects(self, data):
        """Reads all objects from a section"""
        rdr = BytesIO(data)
        while True:
            object_header = rdr.read(5)
            if object_header == b"":
                break
            object_type, size = unpack("<BI", object_header)
            self.objects.append(self.parse_object(object_type, rdr.read(size)))
        rdr.close()

    def read_sections(self):
        """Reads all sections from a file"""
        while True:
            section_header = self.file.read(9)
            if section_header == b"":
                break
            log.info("Section @ %d", self.file.tell())
            compression, total_len, uncomp = unpack("<BII", section_header)
            log.info("Compression: %s", compression)
            log.info("Total length: %d", total_len)
            log.info("Uncompressed length: %d", uncomp)
            section_length = total_len - 13
            data = self.file.read(section_length)
            self.read_objects(data)
            chksum1 = zlib.adler32(pack("<BII", compression, total_len, uncomp) + data)
            chksum2 = unpack("<I", self.file.read(4))[0]
            if chksum1 != chksum2:
                log.error("Checksums do not match, file may be corrupt")
                return
            log.info("Checksum validated successfully")

    def get_object_by_id(self, obj_id):
        """Returns an object based on id"""
        return self.objects[obj_id - 1]
