"""Triangle Strip Array Class"""
from struct import unpack
from ..util import obj2str
from .object3d import Object3D


class TriangleStripArray(Object3D):
    """
    TriangleStripArray defines an array of triangle strips
    """

    def __init__(self):
        super().__init__()
        self.encoding = None
        self.start_index = None
        self.indices = []
        self.strip_lengths = []

    def __str__(self):
        return obj2str(
            "TriangleStripArray",
            [
                ("Encoding", self.encoding),
                ("Start Index", self.start_index),
                ("Indices", f"Array of {len(self.indices)} items"),
                ("Strip Lengths", f"Array of {len(self.strip_lengths)} items"),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.start_index = 0
        self.encoding = unpack("<B", reader.read(1))[0]
        if self.encoding == 0:
            self.start_index = unpack("<I", reader.read(4))[0]
        elif self.encoding == 1:
            self.start_index = unpack("<B", reader.read(1))[0]
        elif self.encoding == 2:
            self.start_index = unpack("<H", reader.read(2))[0]
        elif self.encoding == 128:
            icount = unpack("<I", reader.read(4))[0]
            for _ in range(icount):
                self.indices.append(unpack("<I", reader.read(4))[0])
        elif self.encoding == 129:
            icount = unpack("<I", reader.read(4))[0]
            for _ in range(icount):
                self.indices.append(unpack("<B", reader.read(1))[0])
        elif self.encoding == 130:
            icount = unpack("<I", reader.read(4))[0]
            for _ in range(icount):
                self.indices.append(unpack("<H", reader.read(2))[0])
        scount = unpack("<I", reader.read(4))[0]
        for _ in range(scount):
            self.strip_lengths.append(unpack("<I", reader.read(4))[0])
