from struct import unpack
from .base import Node


class Camera(Node):
    """
    A scene graph node that defines the position of the viewer in the scene and the
    projection from 3D to 2D
    """

    def __init__(self):
        super().__init__()
        self.projection_type = None
        self.projection_matrix = None
        self.fovy = None
        self.aspect_ratio = None
        self.near = None
        self.far = None

    def read(self, rdr):
        super().read(rdr)
        self.projection_type = unpack("<B", rdr.read(1))[0]
        if self.projection_type == 48:
            self.projection_matrix = unpack("<16f", rdr.read(64))
        else:
            (self.fovy, self.aspect_ratio, self.near, self.far) = unpack(
                "<4f", rdr.read(16)
            )


class Group(Node):
    """
    A scene graph node that stores an unordered set of nodes as its children
    """

    def __init__(self):
        super().__init__()
        self.children = []

    def read(self, rdr):
        super().read(rdr)
        count = unpack("<I", rdr.read(4))[0]
        for _ in range(count):
            self.children.append(unpack("<I", rdr.read(4))[0])


class Light(Node):
    """
    A scene graph node that represents different kinds of light sources
    """

    def __init__(self):
        super().__init__()
        self.attenuation_constant = None
        self.attenuation_linear = None
        self.attenuation_quadratic = None
        self.color = None
        self.mode = None
        self.intensity = None
        self.spot_angle = None
        self.spot_exponent = None

    def read(self, rdr):
        super().read(rdr)
        (
            self.attenuation_constant,
            self.attenuation_linear,
            self.attenuation_quadratic,
        ) = unpack("<3f", rdr.read(12))
        self.color = unpack("<3f", rdr.read(12))
        (self.intensity, self.spot_angle, self.spot_exponent) = unpack(
            "<3f", rdr.read(12)
        )


class Mesh(Node):
    """
    A scene graph node that represents a 3D object defined as a polygonal surface.
    """

    def __init__(self):
        super().__init__()
        self.vertex_buffer = None
        self.submesh_count = None
        self.index_buffer = []
        self.appearance = []

    def read(self, rdr):
        super().read(rdr)
        self.vertex_buffer, self.submesh_count = unpack("<II", rdr.read(8))
        for _ in range(self.submesh_count):
            self.index_buffer.append(unpack("<I", rdr.read(4))[0])
            self.appearance.append(unpack("<I", rdr.read(4))[0])


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

    def read(self, rdr):
        super().read(rdr)
        (
            self.image,
            self.appearance,
            self.is_scaled,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
        ) = unpack("<II?4i", rdr.read(25))
