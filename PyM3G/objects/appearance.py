"""
Contains classes related to appearance
"""
from struct import unpack
from ..util import obj2str, const2str
from .base import Object3D, Transformable


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


class Fog(Object3D):
    """
    An Appearance component encapsulating attributes for fogging
    """

    def __init__(self):
        super().__init__()
        self.color = None
        self.mode = None
        self.density = None
        self.near = None
        self.far = None

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
            (self.near.self.far) = unpack("<2f", reader.read(8))
        # else:
        # log.error("Invalid fog mode")


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


class Texture2D(Transformable):
    """
    An Appearance component encapsulating a two-dimensional texture image and a set of
    attributes specifying how the image is to be applied on submeshes
    """

    def __init__(self):
        super().__init__()
        self.image = None
        self.blend_color = None
        self.blending = None
        self.wrapping_s = None
        self.wrapping_t = None
        self.level_filter = None
        self.image_filter = None

    def __str__(self):
        return obj2str(
            "Texture2D",
            [
                ("Image", self.image),
                ("Blend Color", self.blend_color),
                ("Blending", const2str(self.blending)),
                ("Wrapping S", const2str(self.wrapping_s)),
                ("Wrapping T", const2str(self.wrapping_t)),
                ("Level Filter", const2str(self.level_filter)),
                ("Image Filter", const2str(self.image_filter)),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.image = unpack("<I", reader.read(4))[0]
        self.blend_color = unpack("<3B", reader.read(3))
        (
            self.blending,
            self.wrapping_s,
            self.wrapping_t,
            self.level_filter,
            self.image_filter,
        ) = unpack("<5B", reader.read(5))
