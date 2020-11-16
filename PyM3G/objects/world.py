"""World Class"""
from struct import unpack
from ..util import obj2str
from .group import Group


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
            "World",
            [("Active Camera", self.active_camera), ("Background", self.background)],
        )

    def read(self, reader):
        super().read(reader)
        self.active_camera, self.background = unpack("<II", reader.read(8))
