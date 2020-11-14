from struct import unpack
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

    def read(self, rdr):
        super().read(rdr)
        self.textures = []
        (
            self.layer,
            self.compositing_mode,
            self.fog,
            self.polygon_mode,
            self.material,
            texcount,
        ) = unpack("<B5I", rdr.read(21))
        for _ in range(texcount):
            self.textures.append(unpack("<I", rdr.read(4))[0])


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

    def read(self, rdr):
        super().read(rdr)
        (
            self.depth_test_enabled,
            self.depth_write_enabled,
            self.color_write_enabled,
            self.alpha_write_enabled,
            self.blending,
            self.alpha_threshold,
            self.depth_offset_factor,
            self.depth_offset_units,
        ) = unpack("<4?BBff", rdr.read(14))


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

    def read(self, rdr):
        super().read(rdr)
        self.color = unpack("<3f", rdr.read(12))
        self.mode = unpack("<B", rdr.read(1))[0]
        if self.mode == 80:
            self.density = unpack("<f", rdr.read(4))[0]
        elif self.mode == 81:
            (self.near.self.far) = unpack("<2f", rdr.read(8))
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

    def read(self, rdr):
        super().read(rdr)
        self.ambient_color = unpack("<3B", rdr.read(3))
        self.diffuse_color = unpack("<4B", rdr.read(4))
        self.emissive_color = unpack("<3B", rdr.read(3))
        self.specular_color = unpack("<3B", rdr.read(3))
        (self.shininess, self.vertex_color_tracking_enabled) = unpack(
            "<f?", rdr.read(5)
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

    def read(self, rdr):
        super().read(rdr)
        (
            self.culling,
            self.shading,
            self.winding,
            self.two_sided_lighting_enabled,
            self.local_camera_lighting_enabled,
            self.perspective_correction_enabled,
        ) = unpack("<3B3?", rdr.read(6))


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

    def read(self, rdr):
        super().read(rdr)
        self.image = unpack("<I", rdr.read(4))[0]
        self.blend_color = unpack("<3B", rdr.read(3))
        (
            self.blending,
            self.wrapping_s,
            self.wrapping_t,
            self.level_filter,
            self.image_filter,
        ) = unpack("<5B", rdr.read(5))
