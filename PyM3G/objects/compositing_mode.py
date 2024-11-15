"""Compositing Mode Class"""

from struct import unpack
from PyM3G.util import obj2str, const2str
from PyM3G.objects.object3d import Object3D


class CompositingMode(Object3D):
    """
    An Appearance component encapsulating per-pixel compositing attributes
    """

    def __init__(self):
        super().__init__()
        self.depth_test_enabled = True
        self.depth_write_enabled = True
        self.color_write_enabled = True
        self.alpha_write_enabled = True
        self.blending = 68
        self.alpha_threshold = 0.0
        self.depth_offset_factor = 0.0
        self.depth_offset_units = 0.0

    def __str__(self):
        return obj2str(
            "CompositingMode",
            [
                ("Depth Test Enabled", self.depth_test_enabled),
                ("Depth Write Enabled", self.depth_write_enabled),
                ("Color Write Enabled", self.color_write_enabled),
                ("Alpha Write Enabled", self.alpha_write_enabled),
                ("Blending", const2str(self.blending)),
                ("Alpha Threshold", self.alpha_threshold),
                ("Depth Offset Factor", self.depth_offset_factor),
                ("Depth Offset Units", self.depth_offset_units),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (
            self.depth_test_enabled,
            self.depth_write_enabled,
            self.color_write_enabled,
            self.alpha_write_enabled,
            self.blending,
            self.alpha_threshold,
            self.depth_offset_factor,
            self.depth_offset_units,
        ) = unpack("<4?BBff", reader.read(14))
