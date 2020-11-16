"""Light Class"""
from struct import unpack
from ..util import obj2str, const2str
from .node import Node


class Light(Node):
    """
    A scene graph node that represents different kinds of light sources
    """

    def __init__(self):
        super().__init__()
        self.attenuation_constant = None
        self.attenuation_linear = None
        self.attenuation_quadratic = None
        self.color = None
        self.mode = None
        self.intensity = None
        self.spot_angle = None
        self.spot_exponent = None

    def __str__(self):
        return obj2str(
            "Light",
            [
                ("Attenuation Constant", self.attenuation_constant),
                ("Attenuation Linear", self.attenuation_linear),
                ("Attenuation Quadratic", self.attenuation_quadratic),
                ("Color", self.color),
                ("Mode", const2str(self.mode)),
                ("Intensity", self.intensity),
                ("Spot Angle", self.spot_angle),
                ("Spot Exponent", self.spot_exponent),
            ],
        )

    def read(self, reader):
        super().read(reader)
        (
            self.attenuation_constant,
            self.attenuation_linear,
            self.attenuation_quadratic,
        ) = unpack("<3f", reader.read(12))
        self.color = unpack("<3f", reader.read(12))
        (self.intensity, self.spot_angle, self.spot_exponent) = unpack(
            "<3f", reader.read(12)
        )
