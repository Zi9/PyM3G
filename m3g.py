"""
Module for reading JSR 184 m3g files
"""
from dataclasses import dataclass
from io import BytesIO
from struct import unpack
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")


M3G_SIG = b"\xAB\x4A\x53\x52\x31\x38\x34\xBB\x0D\x0A\x1A\x0A"


@dataclass
class Object3D:
    """
    An abstract base class for all objects that can be part of a 3D
    world
    """

    def __init__(self):
        self.user_id = None
        self.animation_tracks = []
        self.user_parameters = {}

    def read(self, rdr):
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

    def __init__(self):
        super().__init__()
        self.has_component_transform = None
        self.translation = None
        self.scale = None
        self.orientation_angle = None
        self.orientation_axis = None
        self.has_general_transform = None
        self.transform = None

    def read(self, rdr):
        super().read(rdr)
        self.has_component_transform = unpack("<?", rdr.read(1))[0]
        if self.has_component_transform:
            self.translation = unpack("<3f", rdr.read(12))
            self.scale = unpack("<3f", rdr.read(12))
            self.orientation_angle = unpack("<f", rdr.read(4))[0]
            self.orientation_axis = unpack("<3f", rdr.read(12))
        self.has_general_transform = unpack("<?", rdr.read(1))[0]
        if self.has_general_transform:
            self.transform = unpack("<16f", rdr.read(64))


@dataclass
class Node(Transformable):
    """
    An abstract base class for all scene graph nodes
    """

    def __init__(self):
        super().__init__()
        self.enable_rendering = None
        self.enable_picking = None
        self.alpha_factor = None
        self.scope = None
        self.has_alignment = None
        self.z_target = None
        self.y_target = None
        self.z_reference = None
        self.y_reference = None

    def read(self, rdr):
        super().read(rdr)
        (
            self.enable_rendering,
            self.enable_picking,
            self.alpha_factor,
            self.scope,
            self.has_alignment,
        ) = unpack("<??BI?", rdr.read(8))
        if self.has_alignment:
            (self.z_target, self.y_target, self.z_reference, self.y_reference) = unpack(
                "<BBII", rdr.read(10)
            )


@dataclass
class Header:
    """
    Header contains metadata about the file
    """

    def __init__(self):
        self.version_number = None
        self.has_external_references = None
        self.total_file_size = None
        self.approximate_content_size = None
        self.authoring_field = None

    def read(self, rdr):
        self.version_number = unpack("<BB", rdr.read(2))
        (
            self.has_external_references,
            self.total_file_size,
            self.approximate_content_size,
        ) = unpack("<?II", rdr.read(9))
        self.authoring_field = rdr.read().rstrip(b"\x00").decode("utf-8")


@dataclass
class ExternalReference:
    """
    Used for including external files (textures or other scenes)
    """

    def __init__(self):
        self.uri = None

    def read(self, rdr):
        self.uri = rdr.read().rstrip(b"\x00").decode("utf-8")


@dataclass
class AnimationController(Object3D):
    """
    Controls the position, speed and weight of an animation sequence
    """

    def __init__(self):
        super().__init__()
        self.speed = None
        self.weight = None
        self.active_interval_start = None
        self.active_interval_end = None
        self.reference_sequence_time = None
        self.reference_world_time = None

    def read(self, rdr):
        super().read(rdr)
        (
            self.speed,
            self.weight,
            self.active_interval_start,
            self.active_interval_end,
            self.reference_sequence_time,
            self.reference_world_time,
        ) = unpack("<ffIIfI", rdr.read(24))


@dataclass
class AnimationTrack(Object3D):
    """
    Associates a KeyframeSequence with an AnimationController and an animatable
    property
    """

    def __init__(self):
        super().__init__()
        self.keyframe_sequence = None
        self.animation_controller = None
        self.property_id = None

    def read(self, rdr):
        super().read(rdr)
        (self.keyframe_sequence, self.animation_controller, self.property_id) = unpack(
            "<3I", rdr.read(12)
        )


@dataclass
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


@dataclass
class Background(Object3D):
    """
    Defines whether and how to clear the viewport
    """

    def __init__(self):
        super().__init__()
        self.background_color = None
        self.background_image = None
        self.background_image_mode_x = None
        self.background_image_mode_y = None
        self.crop_x = None
        self.crop_y = None
        self.crop_width = None
        self.crop_height = None
        self.depth_clear_enabled = None
        self.color_clear_enabled = None

    def read(self, rdr):
        super().read(rdr)
        self.background_color = unpack("<4f", rdr.read(16))
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
        ) = unpack("<IBB4I??", rdr.read(24))


@dataclass
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


@dataclass
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


@dataclass
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
        else:
            log.error("Invalid fog mode")


@dataclass
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


@dataclass
class Image2D(Object3D):
    """
    A two-dimensional image that can be used as a texture, background or sprite image
    """

    def __init__(self):
        super().__init__()
        self.image_format = None
        self.is_mutable = None
        self.width = None
        self.height = None
        self.palette = []
        self.pixels = []

    def read(self, rdr):
        super().read(rdr)
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
    Encapsulates animation data as a sequence of time-stamped, vector-valued keyframes
    """

    def __init__(self):
        super().__init__()
        self.interpolation = None
        self.repeat_mode = None
        self.encoding = None
        self.duration = None
        self.valid_range_first = None
        self.valid_range_last = None
        self.component_count = None
        self.keyframe_count = None
        self.time = []
        self.vector_value = []
        self.vector_bias = []
        self.vector_scale = []

    def read(self, rdr):
        super().read(rdr)
        (
            self.interpolation,
            self.repeat_mode,
            self.encoding,
            self.duration,
            self.valid_range_first,
            self.valid_range_last,
            self.component_count,
            self.keyframe_count,
        ) = unpack(rdr.read(23), "<3B5I")
        if self.encoding == 0:
            for _ in range(self.keyframe_count):
                self.time.append(unpack(rdr.read(4), "<I")[0])
                self.vector_value.append(
                    unpack(
                        rdr.read(4 * self.component_count), f"<{self.component_count}f"
                    )
                )
        elif self.encoding == 1:
            self.vector_bias = unpack(
                rdr.read(4 * self.component_count), f"<{self.component_count}f"
            )
            self.vector_scale = unpack(
                rdr.read(4 * self.component_count), f"<{self.component_count}f"
            )
            for _ in range(self.keyframe_count):
                self.time.append(unpack(rdr.read(4), "<I")[0])
                self.vector_value.append(
                    unpack(rdr.read(self.component_count), f"<{self.component_count}B")
                )
        elif self.encoding == 2:
            self.vector_bias = unpack(
                rdr.read(4 * self.component_count), f"<{self.component_count}f"
            )
            self.vector_scale = unpack(
                rdr.read(4 * self.component_count), f"<{self.component_count}f"
            )
            for _ in range(self.keyframe_count):
                self.time.append(unpack(rdr.read(4), "<I")[0])
                self.vector_value.append(
                    unpack(
                        rdr.read(2 * self.component_count), f"<{self.component_count}H"
                    )
                )


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
class MorphingMesh(Mesh):
    """
    A scene graph node that represents a vertex morphing polygon mesh
    """

    def __init__(self):
        super().__init__()
        self.morph_target_count = None
        self.morph_target = []
        self.initial_weight = []

    def read(self, rdr):
        super().read(rdr)
        self.morph_target_count = unpack(rdr.read(4), "<I")
        for _ in range(self.morph_target_count):
            morph_target, initial_weight = unpack(8, "<If")
            self.morph_target.append(morph_target)
            self.initial_weight.append(initial_weight)


@dataclass
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


@dataclass
class SkinnedMesh(Mesh):
    """
    A scene graph node that represents a skeletally animated polygon mesh
    """

    def __init__(self):
        super().__init__()
        self.skeleton = None
        self.transform_reference_count = None
        self.transform_node = []
        self.first_vertex = []
        self.vertex_count = []
        self.weight = []

    def read(self, rdr):
        super().read(rdr)
        self.skeleton, self.transform_reference_count = unpack(rdr.read(8), "<II")
        for _ in range(self.transform_reference_count):
            (transform_node, first_vertex, vertex_count, weight) = unpack(
                rdr.read(16), "<3Ii"
            )
            self.transform_node.append(transform_node)
            self.first_vertex.append(first_vertex)
            self.vertex_count.append(vertex_count)
            self.weight.append(weight)


@dataclass
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


@dataclass
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


@dataclass
class TriangleStripArray(Object3D):
    """
    TriangleStripArray defines an array of triangle strips
    """

    def __init__(self):
        super().__init__()
        self.encoding = None
        self.start_index = None
        self.indices = []
        self.strip_lengths = []

    def read(self, rdr):
        super().read(rdr)
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
    An array of integer vectors representing vertex positions, normals, colors or
    texture coordinates
    """

    def __init__(self):
        super().__init__()
        self.component_size = None
        self.component_count = None
        self.encoding = None
        self.vertex_count = None
        self.vertices = []

    def read(self, rdr):
        super().read(rdr)
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
            log.error("Error reading vertex array")
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
    VertexBuffer holds references to VertexArrays that contain the positions, colors,
    normals, and texture coordinates for a set of vertices
    """

    def __init__(self):
        super().__init__()
        self.default_color = None
        self.positions = None
        self.position_bias = None
        self.position_scale = None
        self.normals = None
        self.colors = None
        self.texcoord_array_count = None
        self.tex_coords = []
        self.tex_coord_bias = []
        self.tex_coord_scale = []

    def read(self, rdr):
        super().read(rdr)
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

    def __init__(self):
        super().__init__()
        self.active_camera = None
        self.background = None

    def read(self, rdr):
        super().read(rdr)
        self.active_camera, self.background = unpack("<II", rdr.read(8))


class M3GReader:
    """
    Reader for JSR 184 M3G data files
    """

    def __init__(self, path):
        self.objects = []
        self.file = open(path, "rb")
        if not self.verify_signature():
            log.error("Invalid M3G File")
            self.file.close()
            return
        self.read_sections()
        self.file.close()

    def verify_signature(self):
        """Verify header bytes to make sure this is a valid m3g file"""
        if self.file.read(12) == M3G_SIG:
            return True
        return False

    def parse_object(self, objtype, data):
        rdr = BytesIO(data)
        if objtype == 0:
            obj = Header()
        elif objtype == 1:
            obj = AnimationController()
        elif objtype == 2:
            obj = AnimationTrack()
        elif objtype == 3:
            obj = Appearance()
        elif objtype == 4:
            obj = Background()
        elif objtype == 5:
            obj = Camera()
        elif objtype == 6:
            obj = CompositingMode()
        elif objtype == 7:
            obj = Fog()
        elif objtype == 8:
            obj = PolygonMode()
        elif objtype == 9:
            obj = Group()
        elif objtype == 10:
            obj = Image2D()
        elif objtype == 11:
            obj = TriangleStripArray()
        elif objtype == 12:
            obj = Light()
        elif objtype == 13:
            obj = Material()
        elif objtype == 14:
            obj = Mesh()
        elif objtype == 17:
            obj = Texture2D()
        elif objtype == 18:
            obj = Sprite()
        elif objtype == 20:
            obj = VertexArray()
        elif objtype == 21:
            obj = VertexBuffer()
        elif objtype == 22:
            obj = World()
        elif objtype == 255:
            obj = ExternalReference()
        else:
            obj = None
            log.error("Invalid object type found")
            rdr.close()
            return
        obj.read(rdr)

        bytes_unread = len(rdr.read())
        if not isinstance(obj, str) and bytes_unread > 0:
            log.warning("%s bytes left unread", bytes_unread)
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
            log.info("Section data starting at %s", self.file.tell())
            compression, total_len, uncomp = unpack("<BII", section_header)
            log.info("Compression: %s", compression)
            log.info("Total length: %s", total_len)
            log.info("Uncompressed length: %s", uncomp)
            section_length = total_len - 13
            self.read_objects(self.file.read(section_length))
            self.file.read(4)

    def get_object_by_id(self, obj_id):
        """
        Returns an object based on id
        """
        return self.objects[obj_id - 1]
