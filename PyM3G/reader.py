"""
Module for reading JSR 184 m3g files
"""

from io import BytesIO
from struct import unpack, pack
import zlib

import logging
from rich.logging import RichHandler

from PyM3G.util import M3GStatus

from PyM3G.objects.animation_controller import AnimationController
from PyM3G.objects.animation_track import AnimationTrack
from PyM3G.objects.appearance import Appearance
from PyM3G.objects.background import Background
from PyM3G.objects.camera import Camera
from PyM3G.objects.compositing_mode import CompositingMode
from PyM3G.objects.external_reference import ExternalReference
from PyM3G.objects.fog import Fog
from PyM3G.objects.group import Group
from PyM3G.objects.header import Header
from PyM3G.objects.image2d import Image2D
from PyM3G.objects.keyframe_sequence import KeyframeSequence
from PyM3G.objects.light import Light
from PyM3G.objects.material import Material
from PyM3G.objects.mesh import Mesh
from PyM3G.objects.morphing_mesh import MorphingMesh
from PyM3G.objects.polygon_mode import PolygonMode
from PyM3G.objects.skinned_mesh import SkinnedMesh
from PyM3G.objects.sprite import Sprite
from PyM3G.objects.texture2d import Texture2D
from PyM3G.objects.triangle_strip_array import TriangleStripArray
from PyM3G.objects.vertex_array import VertexArray
from PyM3G.objects.vertex_buffer import VertexBuffer
from PyM3G.objects.world import World

_M3G_SIG = b"\xAB\x4A\x53\x52\x31\x38\x34\xBB\x0D\x0A\x1A\x0A"


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

    log = None

    def __init__(self, path, log_level="WARNING"):
        logging.basicConfig(
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )
        self.log = logging.getLogger("m3g")
        self.log.setLevel(log_level)

        self.status = M3GStatus.FAILED
        self.objects = []
        self.file = open(path, "rb")
        if not self.file:
            self.log.error("Could not open file %s", path)
            return
        if not self.verify_signature():
            self.log.error("Invalid M3G file %s", path)
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
            self.log.error("Invalid object type(%d) found", objtype)
            rdr.close()
            return None
        self.log.info(
            "Found [bold cyan]%s[/] object",
            obj.__class__.__name__,
            extra={"markup": True},
        )
        obj.read(rdr)

        bytes_unread = len(rdr.read())
        if obj is None and bytes_unread > 0:
            self.log.warning("%d bytes left unread", bytes_unread)
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
            self.log.info("Section @ %d", self.file.tell())
            compression, total_len, uncomp = unpack("<BII", section_header)
            self.log.info("Compression: %s", compression)
            self.log.info("Total length: %d", total_len)
            self.log.info("Uncompressed length: %d", uncomp)
            section_length = total_len - 13
            data = self.file.read(section_length)
            self.read_objects(data)
            chksum1 = zlib.adler32(pack("<BII", compression, total_len, uncomp) + data)
            chksum2 = unpack("<I", self.file.read(4))[0]
            if chksum1 != chksum2:
                self.log.error(
                    f"Checksums do not match, file '{self.file.name}' may be corrupt"
                )
                return
            self.log.info("Checksum validated successfully")

    def get_object_by_id(self, obj_id):
        """Returns an object based on id"""
        return self.objects[obj_id - 1]
