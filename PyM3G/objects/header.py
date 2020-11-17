"""Header Class"""
from struct import unpack
from PyM3G.util import obj2str


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
        return obj2str(
            "Header",
            [
                ("Version", f"{self.version[0]}.{self.version[1]}"),
                ("Has external references", self.has_external_references),
                ("Total file size", self.total_file_size),
                ("Approximate content size", self.approximate_content_size),
                ("Authoring field text", f"'{self.authoring_field}'"),
            ],
        )

    def read(self, reader):
        """Read header from file stream"""
        self.version = unpack("<BB", reader.read(2))
        (
            self.has_external_references,
            self.total_file_size,
            self.approximate_content_size,
        ) = unpack("<?II", reader.read(9))
        self.authoring_field = reader.read().rstrip(b"\x00").decode("utf-8")
