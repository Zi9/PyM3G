from struct import unpack
from .base import Object3D


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
        # else:
            # log.error("Error reading vertex array")
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