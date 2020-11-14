"""
Contains miscellaneous classes
"""
from struct import unpack
from ..util import obj2str
from .base import Object3D


class Header:
    """
    Header contains metadata about the file
    """

    def __init__(self):
        self.version = None
        self.has_external_references = None
        self.total_file_size = None
        self.approximate_content_size = None
        self.authoring_field = None

    def __str__(self):
        return obj2str("Header",
                       [("Version", f"{self.version[0]}.{self.version[1]}"),
                        ("Has external references", self.has_external_references),
                        ("Total file size", self.total_file_size),
                        ("Approximate content size", self.approximate_content_size),
                        ("Authoring field text", f"'{self.authoring_field}'")])


    def read(self, reader):
        self.version = unpack("<BB", reader.read(2))
        (
            self.has_external_references,
            self.total_file_size,
            self.approximate_content_size,
        ) = unpack("<?II", reader.read(9))
        self.authoring_field = reader.read().rstrip(b"\x00").decode("utf-8")


class ExternalReference:
    """
    Used for including external files (textures or other scenes)
    """

    def __init__(self):
        self.uri = None

    def __str__(self):
        return obj2str("External Reference",
                       [("URI", self.uri)])

    def read(self, reader):
        self.uri = reader.read().rstrip(b"\x00").decode("utf-8")


class Background(Object3D):
    """
    Defines whether and how to clear the viewport
    """

    def __init__(self):
        super().__init__()
        self.background_color = None
        self.background_image = None
        self.background_image_mode_x = None
        self.background_image_mode_y = None
        self.crop_x = None
        self.crop_y = None
        self.crop_width = None
        self.crop_height = None
        self.depth_clear_enabled = None
        self.color_clear_enabled = None

    def __str__(self):
        return obj2str("Background",
                       [("Color", self.background_color),
                        ("Image", self.background_image),
                        ("Image Mode X", self.background_image_mode_x),
                        ("Image Mode Y", self.background_image_mode_y),
                        ("Crop X", self.crop_x),
                        ("Crop Y", self.crop_y),
                        ("Crop Width", self.crop_width),
                        ("Crop Height", self.crop_height),
                        ("Depth Clear Enabled", self.depth_clear_enabled),
                        ("Color Clear Enabled", self.color_clear_enabled)])

    def read(self, reader):
        super().read(reader)
        self.background_color = unpack("<4f", reader.read(16))
        (
            self.background_image,
            self.background_image_mode_x,
            self.background_image_mode_y,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
            self.depth_clear_enabled,
            self.color_clear_enabled,
        ) = unpack("<IBB4I??", reader.read(24))


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
        return obj2str("Image2D",
                       [("Format", self.image_format),
                        ("Is Mutable", self.is_mutable),
                        ("Size", f"{self.width} x {self.height}"),
                        ("Height", self.height),
                        ("Palette", f"Array of {len(self.palette)} items"),
                        ("Pixels", f"Array of {len(self.pixels)} items")])

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
