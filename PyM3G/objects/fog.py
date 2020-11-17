"""Fog Class"""
from struct import unpack
from ..util import obj2str, const2str
from .object3d import Object3D


class Fog(Object3D):
    """
    An Appearance component encapsulating attributes for fogging
    """

    def __init__(self):
        super().__init__()
        self.color = (0, 0, 0, 0)
        self.mode = 81
        self.density = 1.0
        self.near = 0.0
        self.far = 1.0

    def __str__(self):
        return obj2str(
            "Fog",
            [
                ("Color", self.color),
                ("Mode", const2str(self.mode)),
                ("Density", self.density),
                ("Near", self.near),
                ("Far", self.far),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.color = unpack("<3f", reader.read(12))
        self.mode = unpack("<B", reader.read(1))[0]
        if self.mode == 80:
            self.density = unpack("<f", reader.read(4))[0]
        elif self.mode == 81:
            (self.near, self.far) = unpack("<2f", reader.read(8))
