"""Compositing Mode Class"""
from struct import unpack
from ..util import obj2str, const2str
from .object3d import Object3D


class CompositingMode(Object3D):
    """
    An Appearance component encapsulating per-pixel compositing attributes
    """

    def __init__(self):
        super().__init__()
        self.depth_test_enabled = None
        self.depth_write_enabled = None
        self.color_write_enabled = None
        self.alpha_write_enabled = None
        self.blending = None
        self.alpha_threshold = None
        self.depth_offset_factor = None
        self.depth_offset_units = None

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
