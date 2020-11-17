"""Light Class"""
from struct import unpack
from PyM3G.util import obj2str, const2str
from PyM3G.objects.node import Node


class Light(Node):
    """
    A scene graph node that represents different kinds of light sources
    """

    def __init__(self):
        super().__init__()
        self.attenuation_constant = 1.0
        self.attenuation_linear = 1.0
        self.attenuation_quadratic = 1.0
        self.color = (0, 0, 0, 0)
        self.mode = 129
        self.intensity = 1.0
        self.spot_angle = 45
        self.spot_exponent = 0.0

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
