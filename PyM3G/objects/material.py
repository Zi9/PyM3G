"""Material Class"""
from struct import unpack
from ..util import obj2str
from .object3d import Object3D


class Material(Object3D):
    """
    An Appearance component encapsulating material attributes for lighting computations
    """

    def __init__(self):
        super().__init__()
        self.ambient_color = None
        self.diffuse_color = None
        self.emissive_color = None
        self.specular_color = None
        self.shininess = None
        self.vertex_color_tracking_enabled = None

    def __str__(self):
        return obj2str(
            "Material",
            [
                ("Ambient Color", self.ambient_color),
                ("Diffuse Color", self.diffuse_color),
                ("Emissive Color", self.emissive_color),
                ("Specular Color", self.specular_color),
                ("Shininess", self.shininess),
                ("Vertex Color Tracking Enabled", self.vertex_color_tracking_enabled),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.ambient_color = unpack("<3B", reader.read(3))
        self.diffuse_color = unpack("<4B", reader.read(4))
        self.emissive_color = unpack("<3B", reader.read(3))
        self.specular_color = unpack("<3B", reader.read(3))
        (self.shininess, self.vertex_color_tracking_enabled) = unpack(
            "<f?", reader.read(5)
        )
