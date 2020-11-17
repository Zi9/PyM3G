"""Background Class"""
from struct import unpack
from ..util import obj2str, const2str
from .object3d import Object3D


class Background(Object3D):
    """
    Defines whether and how to clear the viewport
    """

    def __init__(self):
        super().__init__()
        self.background_color = (0, 0, 0, 0)
        self.background_image = None
        self.background_image_mode_x = 32
        self.background_image_mode_y = 32
        self.crop_x = None
        self.crop_y = None
        self.crop_width = None
        self.crop_height = None
        self.depth_clear_enabled = True
        self.color_clear_enabled = True

    def __str__(self):
        return obj2str(
            "Background",
            [
                ("Color", self.background_color),
                ("Image", self.background_image),
                ("Image Mode X", const2str(self.background_image_mode_x)),
                ("Image Mode Y", const2str(self.background_image_mode_y)),
                ("Crop X", self.crop_x),
                ("Crop Y", self.crop_y),
                ("Crop Width", self.crop_width),
                ("Crop Height", self.crop_height),
                ("Depth Clear Enabled", self.depth_clear_enabled),
                ("Color Clear Enabled", self.color_clear_enabled),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.background_color = unpack("<4f", reader.read(16))
        (
            self.background_image,
            self.background_image_mode_x,
            self.background_image_mode_y,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
            self.depth_clear_enabled,
            self.color_clear_enabled,
        ) = unpack("<IBB4I??", reader.read(24))
