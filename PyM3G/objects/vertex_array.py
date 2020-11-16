"""Vertex Array Class"""
from struct import unpack
from ..util import obj2str
from .object3d import Object3D


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

    def __str__(self):
        return obj2str(
            "VertexArray",
            [
                ("Component Size", self.component_size),
                ("Component Count", self.component_count),
                ("Encoding", self.encoding),
                ("Vertex Count", self.vertex_count),
                ("Vertices", f"Array of {len(self.vertices)} items"),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.vertices = []
        (
            self.component_size,
            self.component_count,
            self.encoding,
            self.vertex_count,
        ) = unpack("<3BH", reader.read(5))
        if self.component_size == 1:
            c_t = "b"
            c_s = 1
        elif self.component_size == 2:
            c_t = "h"
            c_s = 2
        elif self.component_size == 4:
            c_t = "f"
            c_s = 4
        # else:
        # log.error("Error reading vertex array")
        if self.encoding == 0:
            for _ in range(self.vertex_count):
                self.vertices.append(
                    unpack(
                        "<" + str(self.component_count) + c_t,
                        reader.read(self.component_count * c_s),
                    )
                )
        elif self.encoding == 1:
            delta = (0, 0, 0, 0)
            for _ in range(self.vertex_count):
                vtx = unpack(
                    "<" + str(self.component_count) + c_t,
                    reader.read(self.component_count * c_s),
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
