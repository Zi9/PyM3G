"""Polygon Mode Class"""
from struct import unpack
from ..util import obj2str, const2str
from .object3d import Object3D


class PolygonMode(Object3D):
    """
    An Appearance component encapsulating polygon-level attributes
    """

    def __init__(self):
        super().__init__()
        self.culling = None
        self.shading = None
        self.winding = None
        self.two_sided_lighting_enabled = None
        self.local_camera_lighting_enabled = None
        self.perspective_correction_enabled = None

    def __str__(self):
        return obj2str(
            "Material",
            [
                ("Culling", const2str(self.culling)),
                ("Shading", const2str(self.shading)),
                ("Winding", const2str(self.winding)),
                ("Two Sided Lighting Enabled", self.two_sided_lighting_enabled),
                ("Local Camera Lighting Enabled", self.local_camera_lighting_enabled),
                ("Perspective Correction Enabled", self.perspective_correction_enabled),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (
            self.culling,
            self.shading,
            self.winding,
            self.two_sided_lighting_enabled,
            self.local_camera_lighting_enabled,
            self.perspective_correction_enabled,
        ) = unpack("<3B3?", reader.read(6))
