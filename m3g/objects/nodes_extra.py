from struct import unpack
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

    def read(self, rdr):
        super().read(rdr)
        self.morph_target_count = unpack(rdr.read(4), "<I")
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
