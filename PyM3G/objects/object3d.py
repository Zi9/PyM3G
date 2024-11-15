"""Object3D Class"""

from struct import unpack, pack


class Object3D:
    """
    An abstract base class for all objects that can be part of a 3D world
    """

    def __init__(self):
        self.user_id = 0
        self.animation_tracks = []
        self.user_parameters = {}

    def read(self, reader):
        """Read object data from an input stream"""
        self.user_id, at_count = unpack("<II", reader.read(8))
        if at_count > 0:
            for _ in range(at_count):
                self.animation_tracks.append(unpack("<I", reader.read(4))[0])
        up_count = unpack("<I", reader.read(4))[0]
        if up_count > 0:
            for _ in range(up_count):
                pid, psz = unpack("<II", reader.read(8))
                self.user_parameters[pid] = reader.read(psz)

    def write(self, writer):
        """Write object data to an output stream"""
        writer.write(pack("<II", self.user_id, len(self.animation_tracks)))
        if len(self.animation_tracks) > 0:
            for track in self.animation_tracks:
                writer.write(pack("<I", track))
        writer.write(pack("<I", len(self.user_parameters)))
        if len(self.user_parameters) > 0:
            for pid, pval in self.user_parameters.items():
                writer.write(pack("<II", pid, len(pval)))
                writer.write(pval)
