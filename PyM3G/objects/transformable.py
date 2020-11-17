"""Transformable Class"""
from struct import unpack
from PyM3G.objects.object3d import Object3D


class Transformable(Object3D):
    """
    An abstract base class for Node and Texture2D, defining common methods
    for manipulating node and texture transformations
    """

    def __init__(self):
        super().__init__()
        self.has_component_transform = None
        self.translation = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.orientation_angle = 0
        self.orientation_axis = None
        self.has_general_transform = None
        self.transform = None

    def read(self, reader):
        super().read(reader)
        self.has_component_transform = unpack("<?", reader.read(1))[0]
        if self.has_component_transform:
            self.translation = unpack("<3f", reader.read(12))
            self.scale = unpack("<3f", reader.read(12))
            self.orientation_angle = unpack("<f", reader.read(4))[0]
            self.orientation_axis = unpack("<3f", reader.read(12))
        self.has_general_transform = unpack("<?", reader.read(1))[0]
        if self.has_general_transform:
            self.transform = unpack("<16f", reader.read(64))
