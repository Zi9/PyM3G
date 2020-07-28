"""
Module for loading JSR 184 m3g files
"""
from dataclasses import dataclass
from io import BytesIO
from struct import unpack
from typing import List, Dict

TypeToStr = {
    0: "Header",
    1: "AnimationController",
    2: "AnimationTrack",
    3: "Appearance",
    4: "Background",
    5: "Camera",
    6: "CompositingMode",
    7: "Fog",
    8: "PolygonMode",
    9: "Group",
    10: "Image2D",
    11: "TriangleStripArray",
    12: "Light",
    13: "Material",
    14: "Mesh",
    15: "MorphingMesh",
    16: "SkinnedMesh",
    17: "Texture2D",
    18: "Sprite",
    19: "KeyframeSequence",
    20: "VertexArray",
    21: "VertexBuffer",
    22: "World",
    255: "External Reference",
}

# Base objects


@dataclass
class Object3D:
    """
    An abstract base class for all objects that can be part of a 3D
    world
    """

    user_id: int
    animation_tracks: List[int]
    user_parameters: Dict

    def __init__(self, rdr):
        self.animation_tracks = []
        self.user_parameters = {}
        self.user_id, at_count = unpack("<II", rdr.read(8))
        for _ in range(at_count):
            self.animation_tracks.append(unpack("<I", rdr.read(4))[0])
        up_count = unpack("<I", rdr.read(4))[0]
        for _ in range(up_count):
            pid, psz = unpack("<II", rdr.read(8))
            self.user_parameters[pid] = rdr.read(psz)


@dataclass
class Transformable(Object3D):
    """
    An abstract base class for Node and Texture2D, defining common methods
    for manipulating node and texture transformations
    """

    has_component_transform: bool
    translation: tuple
    scale: tuple
    orientation_angle: float
    orientation_axis: tuple
    has_general_transform: bool
    transform: tuple

    def __init__(self, rdr):
        super().__init__(rdr)
        self.has_component_transform = unpack("<?", rdr.read(1))[0]
        if self.has_component_transform:
            self.translation = unpack("<3f", rdr.read(12))
            self.scale = unpack("<3f", rdr.read(12))
            self.orientation_angle = unpack("<f", rdr.read(4))[0]
            self.orientation_axis = unpack("<3f", rdr.read(12))
        else:
            self.translation = None
            self.scale = None
            self.orientation_angle = None
            self.orientation_axis = None
        self.has_general_transform = unpack("<?", rdr.read(1))[0]
        if self.has_general_transform:
            self.transform = unpack("<16f", rdr.read(64))
        else:
            self.transform = None


@dataclass
class Node(Transformable):
    """
    An abstract base class for all scene graph nodes
    """

    enable_rendering: bool
    enable_picking: bool
    alpha_factor: int
    scope: int
    has_alignment: bool
    z_target: int
    y_target: int
    z_reference: int
    y_reference: int

    def __init__(self, rdr):
        super().__init__(rdr)
        (
            self.enable_rendering,
            self.enable_picking,
            self.alpha_factor,
            self.scope,
            self.has_alignment,
        ) = unpack("<??BI?", rdr.read(8))
        if self.has_alignment:
            (self.z_target, self.y_target, self.z_reference,
             self.y_reference) = unpack("<BBII", rdr.read(10))
        else:
            self.z_target = None
            self.y_target = None
            self.z_reference = None
            self.y_reference = None


# Object classes


@dataclass
class Header:
    """Header object"""  # TODO: Proper docstring

    version_number: tuple
    has_external_references: bool
    total_file_size: int
    approximate_content_size: int
    authoring_field: str

    def __init__(self, rdr):
        self.version_number = unpack("<BB", rdr.read(2))
        (
            self.has_external_references,
            self.total_file_size,
            self.approximate_content_size,
        ) = unpack("<?II", rdr.read(9))
        self.authoring_field = rdr.read().rstrip(b"\x00").decode("utf-8")


@dataclass
class ExternalReference:
    """ExternalReference object"""  # TODO: Proper docstring

    uri: str

    def __init__(self, rdr):
        self.uri = rdr.read().rstrip(b"\x00").decode("utf-8")


@dataclass
class AnimationController(Object3D):
    """
    Controls the position, speed and weight of an animation sequence
    """

    speed: float
    weight: float
    active_interval_start: int
    active_interval_end: int
    reference_sequence_time: float
    reference_world_time: int


@dataclass
class AnimationTrack(Object3D):
    """
    Associates a KeyframeSequence with an AnimationController and an
    animatable property
    """

    keyframe_sequence: int
    animation_controller: int
    property_id: int


@dataclass
class Appearance(Object3D):
    """
    A set of component objects that define the rendering attributes of a
    Mesh or Sprite3D
    """

    layer: int
    compositing_mode: int
    fog: int
    polygon_mode: int
    material: int
    textures: List[int]

    def __init__(self, rdr):
        super().__init__(rdr)
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


@dataclass
class Background(Object3D):
    """
    Defines whether and how to clear the viewport
    """

    background_color: tuple
    background_image: int
    background_image_mode_x: int
    background_image_mode_y: int
    crop_x: int
    crop_y: int
    crop_width: int
    crop_height: int
    depth_clear_enabled: bool
    color_clear_enabled: bool


@dataclass
class Camera(Node):
    """
    A scene graph node that defines the position of the viewer in the scene
    and the projection from 3D to 2D
    """

    projection_type: int
    projection_matrix: tuple
    fovy: float
    aspect_ratio: float
    near: float
    far: float


@dataclass
class CompositingMode(Object3D):
    """
    An Appearance component encapsulating per-pixel compositing
    attributes
    """

    depth_test_enabled: bool
    depth_write_enabled: bool
    color_write_enabled: bool
    alpha_write_enabled: bool
    blending: int
    alpha_threshold: int
    depth_offset_factor: float
    depth_offset_units: float

    def __init__(self, rdr):
        super().__init__(rdr)
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


@dataclass
class Fog(Object3D):
    """
    An Appearance component encapsulating attributes for fogging
    """

    color: tuple
    mode: int
    density: float
    near: float
    far: float


@dataclass
class Group(Node):
    """
    A scene graph node that stores an unordered set of nodes as its
    children
    """

    children: List[int]

    def __init__(self, rdr):
        super().__init__(rdr)
        self.children = []
        count = unpack("<I", rdr.read(4))[0]
        for _ in range(count):
            self.children.append(unpack("<I", rdr.read(4))[0])


@dataclass
class Image2D(Object3D):
    """
    A two-dimensional image that can be used as a texture, background or
    sprite image
    """

    image_format: int
    is_mutable: bool
    width: int
    height: int
    palette: List[int]
    pixels: List[int]

    def __init__(self, rdr):
        super().__init__(rdr)
        self.palette = []
        self.pixels = []
        (self.image_format, self.is_mutable, self.width, self.height) = unpack(
            "<B?II", rdr.read(10)
        )
        if not self.is_mutable:
            pal = unpack("<I", rdr.read(4))[0]
            for _ in range(pal):
                self.palette.append(unpack("<B", rdr.read(1))[0])
            pxl = unpack("<I", rdr.read(4))[0]
            for _ in range(pxl):
                self.pixels.append(unpack("<B", rdr.read(1))[0])


@dataclass
class KeyframeSequence(Object3D):
    """
    Encapsulates animation data as a sequence of time-stamped, vector-valued
    keyframes
    """

    interpolation: int
    repeat_mode: int
    encoding: int
    duration: int
    valid_range_first: int
    valid_range_last: int
    component_count: int
    keyframe_count: int
    time: List[int]
    vector_value: List[tuple]
    vector_bias: List[tuple]
    vector_scale: List[tuple]


@dataclass
class Light(Node):
    """
    A scene graph node that represents different kinds of light sources
    """

    attenuation_constant: float
    attenuation_linear: float
    attenuation_quadratic: float
    color: tuple
    mode: int
    intensity: float
    spot_angle: float
    spot_exponent: float


@dataclass
class Material(Object3D):
    """
    An Appearance component encapsulating material attributes for lighting
    computations
    """

    ambient_color: tuple
    diffuse_color: tuple
    emissive_color: tuple
    specular_color: tuple
    shininess: float
    vertex_color_tracking_enabled: bool

    def __init__(self, rdr):
        super().__init__(rdr)
        self.ambient_color = unpack("<3B", rdr.read(3))
        self.diffuse_color = unpack("<4B", rdr.read(4))
        self.emissive_color = unpack("<3B", rdr.read(3))
        self.specular_color = unpack("<3B", rdr.read(3))
        (self.shininess, self.vertex_color_tracking_enabled) = unpack(
            "<f?", rdr.read(5)
        )


@dataclass
class Mesh(Node):
    """A scene graph node that represents a 3D object defined as a polygonal
    surface."""

    vertex_buffer: int
    submesh_count: int
    index_buffer: List[int]
    appearance: List[int]

    def __init__(self, rdr):
        super().__init__(rdr)
        self.index_buffer = []
        self.appearance = []
        self.vertex_buffer, self.submesh_count = unpack("<II", rdr.read(8))
        for _ in range(self.submesh_count):
            self.index_buffer.append(unpack("<I", rdr.read(4))[0])
            self.appearance.append(unpack("<I", rdr.read(4))[0])


@dataclass
class MorphingMesh(Mesh):
    """
    A scene graph node that represents a vertex morphing polygon mesh
    """

    morph_target_count: int
    morph_target: List[int]
    initial_weight: List[float]


@dataclass
class PolygonMode(Object3D):
    """
    An Appearance component encapsulating polygon-level attributes
    """

    culling: int
    shading: int
    winding: int
    two_sided_lighting_enabled: bool
    local_camera_lighting_enabled: bool
    perspective_correction_enabled: bool

    def __init__(self, rdr):
        super().__init__(rdr)
        (
            self.culling,
            self.shading,
            self.winding,
            self.two_sided_lighting_enabled,
            self.local_camera_lighting_enabled,
            self.perspective_correction_enabled,
        ) = unpack("<3B3?", rdr.read(6))


@dataclass
class SkinnedMesh(Mesh):
    """
    A scene graph node that represents a skeletally animated polygon mesh
    """

    skeleton: int
    transform_reference_count: int
    transform_node: List[int]
    first_vertex: List[int]
    vertex_count: List[int]
    weight: List[int]


@dataclass
class Sprite(Node):
    """
    A scene graph node that represents a 2-dimensional image with a 3D
    position
    """

    image: int
    appearance: int
    is_scaled: bool
    crop_x: int
    crop_y: int
    crop_width: int
    crop_height: int


@dataclass
class Texture2D(Transformable):
    """
    An Appearance component encapsulating a two-dimensional texture image
    and a set of attributes specifying how the image is to be applied on
    submeshes
    """

    image: int
    blend_color: tuple
    blending: int
    wrapping_s: int
    wrapping_t: int
    level_filter: int
    image_filter: int

    def __init__(self, rdr):
        super().__init__(rdr)
        self.image = unpack("<I", rdr.read(4))[0]
        self.blend_color = unpack("<3B", rdr.read(3))
        (
            self.blending,
            self.wrapping_s,
            self.wrapping_t,
            self.level_filter,
            self.image_filter,
        ) = unpack("<5B", rdr.read(5))


@dataclass
class TriangleStripArray(Object3D):
    """
    TriangleStripArray defines an array of triangle strips
    """

    encoding: int
    start_index: int
    indices: List[int]
    strip_lengths: List[int]

    def __init__(self, rdr):
        super().__init__(rdr)
        self.indices = []
        self.strip_lengths = []
        self.start_index = 0
        self.encoding = unpack("<B", rdr.read(1))[0]
        if self.encoding == 0:
            self.start_index = unpack("<I", rdr.read(4))[0]
        elif self.encoding == 1:
            self.start_index = unpack("<B", rdr.read(1))[0]
        elif self.encoding == 2:
            self.start_index = unpack("<H", rdr.read(2))[0]
        elif self.encoding == 128:
            icount = unpack("<I", rdr.read(4))[0]
            for _ in range(icount):
                self.indices.append(unpack("<I", rdr.read(4))[0])
        elif self.encoding == 129:
            icount = unpack("<I", rdr.read(4))[0]
            for _ in range(icount):
                self.indices.append(unpack("<B", rdr.read(1))[0])
        elif self.encoding == 130:
            icount = unpack("<I", rdr.read(4))[0]
            for _ in range(icount):
                self.indices.append(unpack("<H", rdr.read(2))[0])
        scount = unpack("<I", rdr.read(4))[0]
        for _ in range(scount):
            self.strip_lengths.append(unpack("<I", rdr.read(4))[0])


@dataclass
class VertexArray(Object3D):
    """
    An array of integer vectors representing vertex positions, normals, colors,
    or texture coordinates
    """

    component_size: int
    component_count: int
    encoding: int
    vertex_count: int
    vertices: List[tuple]

    def __init__(self, rdr):
        super().__init__(rdr)
        self.vertices = []
        (
            self.component_size,
            self.component_count,
            self.encoding,
            self.vertex_count,
        ) = unpack("<3BH", rdr.read(5))
        if self.component_size == 1:
            c_t = "b"
            c_s = 1
        elif self.component_size == 2:
            c_t = "h"
            c_s = 2
        elif self.component_size == 4:
            c_t = "f"
            c_s = 4
        else:
            print("Error reading vertex array")
        if self.encoding == 0:
            for _ in range(self.vertex_count):
                self.vertices.append(
                    unpack(
                        "<" + str(self.component_count) + c_t,
                        rdr.read(self.component_count * c_s),
                    )
                )
        elif self.encoding == 1:
            delta = (0, 0, 0, 0)
            for _ in range(self.vertex_count):
                vtx = unpack(
                    "<" + str(self.component_count) + c_t,
                    rdr.read(self.component_count * c_s),
                )
                if self.component_count == 2:
                    tvtx = (delta[0] + vtx[0], delta[1] + vtx[1])
                elif self.component_count == 3:
                    tvtx = (delta[0] + vtx[0], delta[1] + vtx[1], delta[2] + vtx[2])
                elif self.component_count == 4:
                    tvtx = (
                        delta[0] + vtx[0],
                        delta[1] + vtx[1],
                        delta[2] + vtx[2],
                        delta[3] + vtx[3],
                    )
                self.vertices.append(tvtx)
                delta = tvtx


@dataclass
class VertexBuffer(Object3D):
    """
    VertexBuffer holds references to VertexArrays that contain the positions,
    colors, normals, and texture coordinates for a set of vertices
    """

    default_color: tuple
    positions: int
    position_bias: tuple
    position_scale: float
    normals: int
    colors: int
    texcoord_array_count: int
    tex_coords: List[int]
    tex_coord_bias: List[tuple]
    tex_coord_scale: List[float]

    def __init__(self, rdr):
        super().__init__(rdr)
        self.tex_coords = []
        self.tex_coord_bias = []
        self.tex_coord_scale = []
        self.default_color = unpack("<4B", rdr.read(4))
        self.positions = unpack("<I", rdr.read(4))[0]
        self.position_bias = unpack("<3f", rdr.read(12))
        (
            self.position_scale,
            self.normals,
            self.colors,
            self.texcoord_array_count,
        ) = unpack("<f3I", rdr.read(16))
        if self.texcoord_array_count > 0:
            for _ in range(self.texcoord_array_count):
                self.tex_coords.append(unpack("<I", rdr.read(4))[0])
                self.tex_coord_bias.append(unpack("<3f", rdr.read(12)))
                self.tex_coord_scale.append(unpack("<f", rdr.read(4))[0])


@dataclass
class World(Group):
    """
    A special Group node that is a top-level container for scene graphs
    """

    active_camera: int
    background: int

    def __init__(self, rdr):
        super().__init__(rdr)
        self.active_camera, self.background = unpack("<II", rdr.read(8))


class Loader:
    """Base reader class for m3g files"""

    M3G_Signature = b"\xAB\x4A\x53\x52\x31\x38\x34\xBB\x0D\x0A\x1A\x0A"

    objects = []

    def __init__(self, path):
        self.file = open(path, "rb")
        if self.verify_signature():
            print("Got m3g file")
            self.read_sections()
        self.file.close()

    def verify_signature(self):
        """Verify header bytes to make sure this is a valid m3g file"""
        if self.file.read(12) == self.M3G_Signature:
            return True
        return False

    def parse_object(self, objtype, data):
        rdr = BytesIO(data)
        if objtype == 0:
            obj = Header(rdr)
        elif objtype == 3:
            obj = Appearance(rdr)
        elif objtype == 6:
            obj = CompositingMode(rdr)
        elif objtype == 8:
            obj = PolygonMode(rdr)
        elif objtype == 9:
            obj = Group(rdr)
        elif objtype == 10:
            obj = Image2D(rdr)
        elif objtype == 11:
            obj = TriangleStripArray(rdr)
        elif objtype == 13:
            obj = Material(rdr)
        elif objtype == 14:
            obj = Mesh(rdr)
        elif objtype == 17:
            obj = Texture2D(rdr)
        elif objtype == 20:
            obj = VertexArray(rdr)
        elif objtype == 21:
            obj = VertexBuffer(rdr)
        elif objtype == 22:
            obj = World(rdr)
        elif objtype == 255:
            obj = ExternalReference(rdr)
        else:
            obj = TypeToStr[objtype]

        bytes_unread = len(rdr.read())
        if not isinstance(obj, str) and bytes_unread > 0:
            print(f"Bytes left unread {bytes_unread}")
        rdr.close()
        return obj

    def read_objects(self, data):
        """
        Reads all objects from a section
        """
        rdr = BytesIO(data)
        while True:
            object_header = rdr.read(5)
            if object_header == b"":
                break
            object_type, size = unpack("<BI", object_header)
            self.objects.append(self.parse_object(object_type, rdr.read(size)))
        rdr.close()

    def read_sections(self):
        """
        Reads all sections from a file
        """
        while True:
            section_header = self.file.read(9)
            if section_header == b"":
                break
            print(f"Section data starting at {self.file.tell()}")
            compression, total_len, uncomp = unpack("<BII", section_header)
            print(f"Compression: {compression}")
            print(f"Total length: {total_len}")
            print(f"Uncompressed length: {uncomp}")
            section_length = total_len - 13
            self.read_objects(self.file.read(section_length))
            self.file.read(4)
