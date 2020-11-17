"""Texture2D Class"""
from struct import unpack
from ..util import obj2str, const2str
from .transformable import Transformable


class Texture2D(Transformable):
    """
    An Appearance component encapsulating a two-dimensional texture image and a set of
    attributes specifying how the image is to be applied on submeshes
    """

    def __init__(self):
        super().__init__()
        self.image = None
        self.blend_color = (0.0, 0.0, 0.0, 0.0)
        self.blending = 227
        self.wrapping_s = 241
        self.wrapping_t = 241
        self.level_filter = 208
        self.image_filter = 210

    def __str__(self):
        return obj2str(
            "Texture2D",
            [
                ("Image", self.image),
                ("Blend Color", self.blend_color),
                ("Blending", const2str(self.blending)),
                ("Wrapping S", const2str(self.wrapping_s)),
                ("Wrapping T", const2str(self.wrapping_t)),
                ("Level Filter", const2str(self.level_filter)),
                ("Image Filter", const2str(self.image_filter)),
            ],
        )

    def read(self, reader):
        super().read(reader)
        self.image = unpack("<I", reader.read(4))[0]
        self.blend_color = unpack("<3B", reader.read(3))
        (
            self.blending,
            self.wrapping_s,
            self.wrapping_t,
            self.level_filter,
            self.image_filter,
        ) = unpack("<5B", reader.read(5))
