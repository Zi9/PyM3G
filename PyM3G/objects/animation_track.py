"""Animation Track Class"""
from struct import unpack
from PyM3G.util import obj2str, const2str
from PyM3G.objects.object3d import Object3D


class AnimationTrack(Object3D):
    """
    Associates a KeyframeSequence with an AnimationController and an animatable
    property
    """

    def __init__(self):
        super().__init__()
        self.keyframe_sequence = None
        self.animation_controller = None
        self.property_id = None

    def __str__(self):
        return obj2str(
            "AnimationTrack",
            [
                ("Keyframe Sequence", self.keyframe_sequence),
                ("Animation Controller", self.animation_controller),
                ("Property ID", const2str(self.property_id)),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (self.keyframe_sequence, self.animation_controller, self.property_id) = unpack(
            "<3I", reader.read(12)
        )
