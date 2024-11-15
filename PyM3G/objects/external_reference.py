"""External Reference Class"""

from PyM3G.util import obj2str


class ExternalReference:
    """
    Used for including external files (textures or other scenes)
    """

    def __init__(self):
        self.uri = None

    def __str__(self):
        return obj2str("External Reference", [("URI", self.uri)])

    def read(self, reader):
        """Read external reference string from file stream"""
        self.uri = reader.read().rstrip(b"\x00").decode("utf-8")
