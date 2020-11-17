"""Morphing Mesh Class"""
from struct import unpack
from PyM3G.util import obj2str
from PyM3G.objects.mesh import Mesh


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
                ("Initial Weight", f"Array of {len(self.initial_weight)} items"),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.morph_target_count = unpack(reader.read(4), "<I")
        for _ in range(self.morph_target_count):
            morph_target, initial_weight = unpack(8, "<If")
            self.morph_target.append(morph_target)
            self.initial_weight.append(initial_weight)
