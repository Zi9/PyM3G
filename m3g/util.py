from enum import Enum, auto


class M3GStatus(Enum):
    """Enum for different Reader and Writer status codes"""
    SUCCESS = auto()
    FAILED = auto()
    CHECKSUM_FAIL = auto()


def obj2str(obtype, values):
    typeprinted = False
    typesize = len(obtype) + 4
    outstr = ""
    for item in values:
        if not typeprinted:
            outstr += f"{obtype} -> {item[0]}: {item[1]}\n"
            typeprinted = True
        else:
            outstr += " " * typesize + f"{item[0]}: {item[1]}\n"
    return outstr
