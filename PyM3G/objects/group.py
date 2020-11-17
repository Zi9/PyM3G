"""Group Class"""
from struct import unpack
from PyM3G.util import obj2str
from PyM3G.objects.node import Node


class Group(Node):
    """
    A scene graph node that stores an unordered set of nodes as its children
    """

    def __init__(self):
        super().__init__()
        self.children = []

    def __str__(self):
        return obj2str("Group", [("Children", self.children)])

    def read(self, reader):
        super().read(reader)
        count = unpack("<I", reader.read(4))[0]
        for _ in range(count):
            self.children.append(unpack("<I", reader.read(4))[0])
