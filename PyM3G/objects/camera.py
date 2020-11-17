"""Camera Class"""
from struct import unpack
from ..util import obj2str, const2str
from .node import Node


class Camera(Node):
    """
    A scene graph node that defines the position of the viewer in the scene and the
    projection from 3D to 2D
    """

    def __init__(self):
        super().__init__()
        self.projection_type = 48
        self.projection_matrix = None
        self.fovy = None
        self.aspect_ratio = None
        self.near = None
        self.far = None

    def __str__(self):
        return obj2str(
            "Camera",
            [
                ("Projection Type", const2str(self.projection_type)),
                ("Projection Matrix", self.projection_matrix),
                ("Fov Y", self.fovy),
                ("Aspect Ratio", self.aspect_ratio),
                ("Near", self.near),
                ("Far", self.far),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.projection_type = unpack("<B", reader.read(1))[0]
        if self.projection_type == 48:
            self.projection_matrix = unpack("<16f", reader.read(64))
        else:
            (self.fovy, self.aspect_ratio, self.near, self.far) = unpack(
                "<4f", reader.read(16)
            )
