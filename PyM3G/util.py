"""Utility functions"""

from enum import Enum, auto


_constants = {
    2: "ANTIALIAS",
    4: "DITHER",
    8: "TRUE_COLOR",
    16: "OVERWRITE",
    32: "BORDER",
    33: "REPEAT",
    48: "GENERIC",
    49: "PARALLEL",
    50: "PERSPECTIVE",
    64: "ALPHA",
    65: "ALPHA_ADD",
    66: "MODULATE",
    67: "MODULATE_X2",
    68: "REPLACE",
    80: "EXPONENTIAL",
    81: "LINEAR",
    96: "ALPHA",
    97: "LUMINANCE",
    98: "LUMINANCE_ALPHA",
    99: "RGB",
    100: "RGBA",
    128: "AMBIENT",
    129: "DIRECTIONAL",
    130: "OMNI",
    131: "SPOT",
    144: "NONE",
    145: "ORIGIN",
    146: "X_AXIS",
    147: "Y_AXIS",
    148: "Z_AXIS",
    160: "CULL_BACK",
    161: "CULL_FRONT",
    162: "CULL_NONE",
    164: "SHADE_FLAT",
    165: "SHADE_SMOOTH",
    168: "WINDING_CCW",
    169: "WINDING_CW",
    176: "LINEAR",
    177: "SLERP",
    178: "SPLINE",
    179: "SQUAD",
    180: "STEP",
    192: "CONSTANT",
    193: "LOOP",
    208: "FILTER_BASE_LEVEL",
    209: "FILTER_LINEAR",
    210: "FILTER_NEAREST",
    224: "FUNC_ADD",
    225: "FUNC_BLEND",
    226: "FUNC_DECAL",
    227: "FUNC_MODULATE",
    228: "FUNC_REPLACE",
    240: "WRAP_CLAMP",
    241: "WRAP_REPEAT",
    256: "ALPHA",
    257: "AMBIENT_COLOR",
    258: "COLOR",
    259: "CROP",
    260: "DENSITY",
    261: "DIFFUSE_COLOR",
    262: "EMISSIVE_COLOR",
    263: "FAR_DISTANCE",
    264: "FIELD_OF_VIEW",
    265: "INTENSITY",
    266: "MORPH_WEIGHTS",
    267: "NEAR_DISTANCE",
    268: "ORIENTATION",
    269: "PICKABILITY",
    270: "SCALE",
    271: "SHININESS",
    272: "SPECULAR_COLOR",
    273: "SPOT_ANGLE",
    274: "SPOT_EXPONENT",
    275: "TRANSLATION",
    276: "VISIBILITY",
    1024: "AMBIENT",
    2048: "DIFFUSE",
    4096: "EMISSIVE",
    8192: "SPECULAR",
}


class M3GStatus(Enum):
    """Enum for different Reader and Writer status codes"""

    SUCCESS = auto()
    FAILED = auto()
    CHECKSUM_FAIL = auto()


def obj2str(obtype, values):
    """Build a string representation of an object"""
    outstr = f"{obtype}:\n"
    for item in values:
        outstr += f"\t{item[0]}: {item[1]}\n"
    return outstr


def const2str(const_id):
    """Return a string representing a constant value"""
    return _constants.get(const_id)
