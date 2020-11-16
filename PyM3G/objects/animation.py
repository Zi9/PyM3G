"""
Contains classes related to animation
"""
from struct import unpack
from ..util import obj2str, const2str
from .base import Object3D


class AnimationController(Object3D):
    """
    Controls the position, speed and weight of an animation sequence
    """

    def __init__(self):
        super().__init__()
        self.speed = 1.0
        self.weight = 1.0
        self.active_interval_start = 0
        self.active_interval_end = 0
        self.reference_sequence_time = 0
        self.reference_world_time = 0

    def __str__(self):
        return obj2str(
            "AnimationController",
            [
                ("Speed", self.speed),
                ("Weight", self.weight),
                ("Active Interval Start", self.active_interval_start),
                ("Active Interval End", self.active_interval_end),
                ("Reference Sequence Time", self.reference_sequence_time),
                ("Reference World Time", self.reference_world_time),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (
            self.speed,
            self.weight,
            self.active_interval_start,
            self.active_interval_end,
            self.reference_sequence_time,
            self.reference_world_time,
        ) = unpack("<ffIIfI", reader.read(24))


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


class KeyframeSequence(Object3D):
    """
    Encapsulates animation data as a sequence of time-stamped, vector-valued keyframes
    """

    def __init__(self):
        super().__init__()
        self.interpolation = None
        self.repeat_mode = None
        self.encoding = None
        self.duration = None
        self.valid_range_first = None
        self.valid_range_last = None
        self.component_count = None
        self.keyframe_count = None
        self.time = []
        self.vector_value = []
        self.vector_bias = []
        self.vector_scale = []

    def __str__(self):
        return obj2str(
            "KeyframeSequence",
            [
                ("Interpolation", const2str(self.interpolation)),
                ("Repeat Mode", const2str(self.repeat_mode)),
                ("Encoding", self.encoding),
                ("Duration", self.duration),
                ("Valid Range First", self.valid_range_first),
                ("Valid Range Last", self.valid_range_last),
                ("Component Count", self.component_count),
                ("Keyframe Count", self.keyframe_count),
                ("Time", f"Array of {len(self.time)} items"),
                ("Vector Value", f"Array of {len(self.vector_value)} items"),
                ("Vector Bias", f"Array of {len(self.vector_bias)} items"),
                ("Vector Scale", f"Array of {len(self.vector_scale)} items"),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (
            self.interpolation,
            self.repeat_mode,
            self.encoding,
            self.duration,
            self.valid_range_first,
            self.valid_range_last,
            self.component_count,
            self.keyframe_count,
        ) = unpack(reader.read(23), "<3B5I")
        if self.encoding == 0:
            for _ in range(self.keyframe_count):
                self.time.append(unpack(reader.read(4), "<I")[0])
                self.vector_value.append(
                    unpack(
                        reader.read(4 * self.component_count),
                        f"<{self.component_count}f",
                    )
                )
        elif self.encoding == 1:
            self.vector_bias = unpack(
                reader.read(4 * self.component_count), f"<{self.component_count}f"
            )
            self.vector_scale = unpack(
                reader.read(4 * self.component_count), f"<{self.component_count}f"
            )
            for _ in range(self.keyframe_count):
                self.time.append(unpack(reader.read(4), "<I")[0])
                self.vector_value.append(
                    unpack(
                        reader.read(self.component_count), f"<{self.component_count}B"
                    )
                )
        elif self.encoding == 2:
            self.vector_bias = unpack(
                reader.read(4 * self.component_count), f"<{self.component_count}f"
            )
            self.vector_scale = unpack(
                reader.read(4 * self.component_count), f"<{self.component_count}f"
            )
            for _ in range(self.keyframe_count):
                self.time.append(unpack(reader.read(4), "<I")[0])
                self.vector_value.append(
                    unpack(
                        reader.read(2 * self.component_count),
                        f"<{self.component_count}H",
                    )
                )
