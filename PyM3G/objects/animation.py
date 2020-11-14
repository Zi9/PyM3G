"""
Contains classes related to animation
"""
from struct import unpack
from .base import Object3D


class AnimationController(Object3D):
    """
    Controls the position, speed and weight of an animation sequence
    """

    def __init__(self):
        super().__init__()
        self.speed = None
        self.weight = None
        self.active_interval_start = None
        self.active_interval_end = None
        self.reference_sequence_time = None
        self.reference_world_time = None

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
