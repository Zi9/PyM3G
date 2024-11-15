"""Image2D Class"""

from struct import unpack
from PyM3G.util import obj2str, const2str
from PyM3G.objects.object3d import Object3D


class Image2D(Object3D):
    """
    A two-dimensional image that can be used as a texture, background or sprite image
    """

    def __init__(self):
        super().__init__()
        self.image_format = None
        self.is_mutable = None
        self.width = None
        self.height = None
        self.palette = []
        self.pixels = []

    def __str__(self):
        return obj2str(
            "Image2D",
            [
                ("Format", const2str(self.image_format)),
                ("Is Mutable", self.is_mutable),
                ("Size", f"{self.width} x {self.height}"),
                ("Height", self.height),
                ("Palette", f"Array of {len(self.palette)} items"),
                ("Pixels", f"Array of {len(self.pixels)} items"),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (self.image_format, self.is_mutable, self.width, self.height) = unpack(
            "<B?II", reader.read(10)
        )
        if not self.is_mutable:
            pal = unpack("<I", reader.read(4))[0]
            for _ in range(pal):
                self.palette.append(unpack("<B", reader.read(1))[0])
            pxl = unpack("<I", reader.read(4))[0]
            for _ in range(pxl):
                self.pixels.append(unpack("<B", reader.read(1))[0])
