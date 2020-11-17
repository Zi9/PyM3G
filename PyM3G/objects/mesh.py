"""Mesh Class"""
from struct import unpack
from PyM3G.util import obj2str
from PyM3G.objects.node import Node


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

    def __str__(self):
        return obj2str(
            "Mesh",
            [
                ("Vertex Buffer", self.vertex_buffer),
                ("Submesh Count", self.submesh_count),
                ("Index Buffer", self.index_buffer),
                ("Appearance", self.appearance),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.vertex_buffer, self.submesh_count = unpack("<II", reader.read(8))
        for _ in range(self.submesh_count):
            self.index_buffer.append(unpack("<I", reader.read(4))[0])
            self.appearance.append(unpack("<I", reader.read(4))[0])
