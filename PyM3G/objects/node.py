"""Node Class"""
from struct import unpack
from .transformable import Transformable


class Node(Transformable):
    """
    An abstract base class for all scene graph nodes
    """

    def __init__(self):
        super().__init__()
        self.enable_rendering = True
        self.enable_picking = True
        self.alpha_factor = 1.0
        self.scope = -1
        self.has_alignment = None
        self.z_target = None
        self.y_target = None
        self.z_reference = None
        self.y_reference = None

    def read(self, reader):
        super().read(reader)
        (
            self.enable_rendering,
            self.enable_picking,
            self.alpha_factor,
            self.scope,
            self.has_alignment,
        ) = unpack("<??BI?", reader.read(8))
        if self.has_alignment:
            (self.z_target, self.y_target, self.z_reference, self.y_reference) = unpack(
                "<BBII", reader.read(10)
            )
        self.alpha_factor = self.alpha_factor / 255.0
