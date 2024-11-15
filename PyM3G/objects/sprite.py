"""Sprite Class"""

from struct import unpack
from PyM3G.util import obj2str
from PyM3G.objects.node import Node


class Sprite(Node):
    """
    A scene graph node that represents a 2-dimensional image with a 3D position
    """

    def __init__(self):
        super().__init__()
        self.image = None
        self.appearance = None
        self.is_scaled = None
        self.crop_x = None
        self.crop_y = None
        self.crop_width = None
        self.crop_height = None

    def __str__(self):
        return obj2str(
            "Sprite",
            [
                ("Image", self.image),
                ("Appearance", self.appearance),
                ("Is Scaled", self.is_scaled),
                ("Crop X", self.crop_x),
                ("Crop Y", self.crop_y),
                ("Crop Width", self.crop_width),
                ("Crop Height", self.crop_height),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (
            self.image,
            self.appearance,
            self.is_scaled,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
        ) = unpack("<II?4i", reader.read(25))
