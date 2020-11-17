"""Vertex Buffer Class"""
from struct import unpack
from PyM3G.util import obj2str
from PyM3G.objects.object3d import Object3D


class VertexBuffer(Object3D):
    """
    VertexBuffer holds references to VertexArrays that contain the positions, colors,
    normals, and texture coordinates for a set of vertices
    """

    def __init__(self):
        super().__init__()
        self.default_color = (1.0, 1.0, 1.0, 1.0)
        self.positions = None
        self.position_bias = None
        self.position_scale = None
        self.normals = None
        self.colors = None
        self.texcoord_array_count = None
        self.tex_coords = []
        self.tex_coord_bias = []
        self.tex_coord_scale = []

    def __str__(self):
        return obj2str(
            "VertexBuffer",
            [
                ("Default Color", self.default_color),
                ("Positions", self.positions),
                ("Position Bias", self.position_bias),
                ("Position Scale", self.position_scale),
                ("Normals", self.normals),
                ("Colors", self.colors),
                ("Texcoord Array Count", self.texcoord_array_count),
                ("Texcoords", f"Array of {len(self.tex_coords)} items"),
                ("Texcoord Bias", f"Array of {len(self.tex_coord_bias)} items"),
                ("Texcoord Scale", f"Array of {len(self.tex_coord_scale)} items"),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.default_color = unpack("<4B", reader.read(4))
        self.positions = unpack("<I", reader.read(4))[0]
        self.position_bias = unpack("<3f", reader.read(12))
        (
            self.position_scale,
            self.normals,
            self.colors,
            self.texcoord_array_count,
        ) = unpack("<f3I", reader.read(16))
        if self.texcoord_array_count > 0:
            for _ in range(self.texcoord_array_count):
                self.tex_coords.append(unpack("<I", reader.read(4))[0])
                self.tex_coord_bias.append(unpack("<3f", reader.read(12)))
                self.tex_coord_scale.append(unpack("<f", reader.read(4))[0])
