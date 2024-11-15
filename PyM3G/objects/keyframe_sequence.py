"""Keyframe Sequence Class"""

from struct import unpack
from PyM3G.util import obj2str, const2str
from PyM3G.objects.object3d import Object3D


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
