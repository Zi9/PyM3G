"""Appearance Class"""
from struct import unpack
from ..util import obj2str
from .object3d import Object3D


class Appearance(Object3D):
    """
    A set of component objects that define the rendering attributes of a Mesh or
    Sprite3D
    """

    def __init__(self):
        super().__init__()
        self.layer = None
        self.compositing_mode = None
        self.fog = None
        self.polygon_mode = None
        self.material = None
        self.textures = []

    def __str__(self):
        return obj2str(
            "Appearance",
            [
                ("Layer", self.layer),
                ("Compositing Mode", self.compositing_mode),
                ("Fog", self.fog),
                ("Polygon Mode", self.polygon_mode),
                ("Material", self.material),
                ("Textures", self.textures),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.textures = []
        (
            self.layer,
            self.compositing_mode,
            self.fog,
            self.polygon_mode,
            self.material,
            texcount,
        ) = unpack("<B5I", reader.read(21))
        for _ in range(texcount):
            self.textures.append(unpack("<I", reader.read(4))[0])
