"""
Contains base classes for objects
"""
from struct import unpack


class Object3D:
    """
    An abstract base class for all objects that can be part of a 3D
    world
    """

    def __init__(self):
        self.user_id = None
        self.animation_tracks = []
        self.user_parameters = {}

    def read(self, reader):
        self.user_id, at_count = unpack("<II", reader.read(8))
        for _ in range(at_count):
            self.animation_tracks.append(unpack("<I", reader.read(4))[0])
        up_count = unpack("<I", reader.read(4))[0]
        for _ in range(up_count):
            pid, psz = unpack("<II", reader.read(8))
            self.user_parameters[pid] = reader.read(psz)


class Transformable(Object3D):
    """
    An abstract base class for Node and Texture2D, defining common methods
    for manipulating node and texture transformations
    """

    def __init__(self):
        super().__init__()
        self.has_component_transform = None
        self.translation = None
        self.scale = None
        self.orientation_angle = None
        self.orientation_axis = None
        self.has_general_transform = None
        self.transform = None

    def read(self, reader):
        super().read(reader)
        self.has_component_transform = unpack("<?", reader.read(1))[0]
        if self.has_component_transform:
            self.translation = unpack("<3f", reader.read(12))
            self.scale = unpack("<3f", reader.read(12))
            self.orientation_angle = unpack("<f", reader.read(4))[0]
            self.orientation_axis = unpack("<3f", reader.read(12))
        self.has_general_transform = unpack("<?", reader.read(1))[0]
        if self.has_general_transform:
            self.transform = unpack("<16f", reader.read(64))


class Node(Transformable):
    """
    An abstract base class for all scene graph nodes
    """

    def __init__(self):
        super().__init__()
        self.enable_rendering = None
        self.enable_picking = None
        self.alpha_factor = None
        self.scope = None
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
