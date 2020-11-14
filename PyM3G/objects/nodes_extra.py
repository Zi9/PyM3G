"""
Contains subclasses of scenegraph node classes
"""
from struct import unpack
from ..util import obj2str
from .nodes import Group, Mesh


class MorphingMesh(Mesh):
    """
    A scene graph node that represents a vertex morphing polygon mesh
    """

    def __init__(self):
        super().__init__()
        self.morph_target_count = None
        self.morph_target = []
        self.initial_weight = []

    def __str__(self):
        return obj2str(
            "MorphingMesh",
            [
                ("Morph Target Count", self.morph_target_count),
                ("Morph Target", f"Array of {len(self.morph_target)} items"),
                ("Initial Weight", f"Array of {len(self.initial_weight)} items")
            ]
        )

    def read(self, reader):
        super().read(reader)
        self.morph_target_count = unpack(reader.read(4), "<I")
        for _ in range(self.morph_target_count):
            morph_target, initial_weight = unpack(8, "<If")
            self.morph_target.append(morph_target)
            self.initial_weight.append(initial_weight)


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

    def __str__(self):
        return obj2str(
            "SkinnedMesh",
            [
                ("Skeleton", self.skeleton),
                ("Transform Reference Count", self.transform_reference_count),
                ("Transform Node", f"Array of {len(self.transform_node)} items"),
                ("First Vertex", f"Array of {len(self.first_vertex)} items"),
                ("Vertex Count", f"Array of {len(self.vertex_count)} items"),
                ("Weight", f"Array of {len(self.weight)} items")
            ]
        )

    def read(self, reader):
        super().read(reader)
        self.skeleton, self.transform_reference_count = unpack(reader.read(8), "<II")
        for _ in range(self.transform_reference_count):
            (transform_node, first_vertex, vertex_count, weight) = unpack(
                reader.read(16), "<3Ii"
            )
            self.transform_node.append(transform_node)
            self.first_vertex.append(first_vertex)
            self.vertex_count.append(vertex_count)
            self.weight.append(weight)


class World(Group):
    """
    A special Group node that is a top-level container for scene graphs
    """

    def __init__(self):
        super().__init__()
        self.active_camera = None
        self.background = None

    def __str__(self):
        return obj2str(
            "World", [
                ("Active Camera", self.active_camera),
                ("Background", self.background)
            ]
        )

    def read(self, reader):
        super().read(reader)
        self.active_camera, self.background = unpack("<II", reader.read(8))
