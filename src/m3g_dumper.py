"""M3G Dumper utility - dumps contents of JSR 184 3d files"""
from dataclasses import dataclass
from io import BytesIO
from struct import unpack
from typing import List, Dict
import timeit

ObjTypeNames = {
    0: 'Header',
    1: "AnimationController",
    2: "AnimationTrack",
    3: "Appearance",
    4: "Background",
    5: "Camera",
    6: "CompositingMode",
    7: "Fog",
    8: "PolygonMode",
    9: "Group",
    10: "Image2D",
    11: "TriangleStripArray",
    12: "Light",
    13: "Material",
    14: "Mesh",
    15: "MorphingMesh",
    16: "SkinnedMesh",
    17: "Texture2D",
    18: "Sprite",
    19: "KeyframeSequence",
    20: "VertexArray",
    21: "VertexBuffer",
    22: "World",
    255: "External Reference"
}


@dataclass
class Object3D:
    """An abstract base class for all objects that can be part of a 3D
    world. """
    user_id: int
    animation_tracks: List[int] = []
    user_parameters: Dict = {}


@dataclass
class Transformable(Object3D):
    """An abstract base class for Node and Texture2D, defining common methods
    for manipulating node and texture transformations."""
    has_component_transform: bool
    translation: tuple = None
    scale: tuple = None
    orientation_angle: float = None
    orientation_axis: tuple = None
    has_general_transform: bool
    transform: tuple = None


@dataclass
class Node(Transformable):
    """An abstract base class for all scene graph nodes."""
    enable_rendering: bool
    enable_picking: bool
    alpha_factor: int
    scope: int
    has_alignment: bool
    z_target: int = None
    y_target: int = None
    z_reference: int = None
    y_reference: int = None


@dataclass
class Header:
    """Header object"""  # TODO: Proper docstring
    version_number: tuple = None
    has_external_references: bool = None
    total_file_size: int = None
    approximate_content_size: int = None
    authoring_field: str = None


@dataclass
class AnimationController(Object3D):
    """Controls the position, speed and weight of an animation sequence."""
    speed: float
    weight: float
    active_interval_start: int
    active_interval_end: int
    reference_sequence_time: float
    reference_world_time: int


@dataclass
class AnimationTrack(Object3D):
    """Associates a KeyframeSequence with an AnimationController and an
    animatable property."""
    keyframe_sequence: int
    animation_controller: int
    property_id: int


@dataclass
class Appearance(Object3D):
    """A set of component objects that define the rendering attributes of a
    Mesh or Sprite3D."""
    layer: int
    compositing_mode: int
    fog: int
    polygon_mode: int
    material: int
    textures: List[int] = []


@dataclass
class Background(Object3D):
    """Defines whether and how to clear the viewport."""
    background_color: tuple
    background_image: int
    background_image_mode_x: int
    background_image_mode_y: int
    crop_x: int
    crop_y: int
    crop_width: int
    crop_height: int
    depth_clear_enabled: bool
    color_clear_enabled: bool


class Loader:
    """Base reader class for m3g files"""
    M3G_Signature = b'\xAB\x4A\x53\x52\x31\x38\x34\xBB\x0D\x0A\x1A\x0A'

    objects = []

    def __init__(self, path):
        self.file = open(path, 'rb')
        if self.VerifySignature():
            print('Got m3g file')
            self.ReadSections()
        self.file.close()

    def VerifySignature(self):
        """Verify header bytes to make sure this is a valid m3g file"""
        if self.file.read(12) == self.M3G_Signature:
            return True
        return False

    def ReadObject3D(self, rdr):
        uid, aCount = unpack('<II', rdr.read(8))
        if aCount > 0:
            animTracks = unpack('<' + str(aCount) + 'I', rdr.read(aCount*4))
        else:
            animTracks = None
        uparamCount = unpack('<I', rdr.read(4))[0]
        if uparamCount > 0:
            params = []
            for i in range(uparamCount):
                paramID, sz = unpack('<II', rdr.read(8))
                val = unpack('<' + str(sz) + 'c')
                params.append((paramID, val))
        else:
            params = None
        return Object3D(uid, animTracks, params)

    def ReadTransformable(self, rdr):
        sup = self.ReadObject3D(rdr)
        compTransf = unpack('<?', rdr.read(1))
        if compTransf:
            translation = unpack('<fff', rdr.read(12))
            scale = unpack('<fff', rdr.read(12))
            orientAngle = unpack('<f', rdr.read(4))[0]
            orientAxis = unpack('<fff', rdr.read(12))
        genTransf = unpack('<?', rdr.read(1))[0]
        if genTransf:
            mtrx = unpack('<16f', rdr.read(64))
        tr = Transformable(sup, compTransf, translation, scale, orientAngle,
                           orientAxis, genTransf, mtrx)
        return tr

    def ReadNode(self, rdr):
        sup = self.ReadTransformable(rdr)
        render, pick, alpha, scope, align = unpack('<??BI?', rdr.read(8))
        if align:
            zt, yt, zr, yr = unpack('<BBII', rdr.read(10))
        else:
            zt = None
            yt = None
            zr = None
            yr = None
        nd = Node(sup, render, pick, alpha, scope, align, zt, yt, zr, yr)
        return nd

    def ParseObject(self, objtype, data):
        rdr = BytesIO(data)
        if objtype == 0:
            verMa, verMi, refs, size = unpack('<BB?I4x', rdr.read(11))
            authoring = rdr.read().rstrip(b'\x00').decode('utf-8')
            hdr = Header(f'{verMa}.{verMi}', size, refs, authoring)
            rdr.close()
            return hdr
        elif objtype == 8:
            s_class = self.ReadObject3D(rdr)
            d = unpack('<BBB???', rdr.read(6))
            pmode = PolygonMode(s_class, d[0], d[1], d[2], d[3], d[4], d[5])
            rdr.close()
            return pmode
        elif objtype == 17:
            s_class = self.ReadTransformable(rdr)
            img = unpack('<I', rdr.read(4))[0]
            bcol = unpack('<BBB', rdr.read(3))
            blend, wrpS, wrpT, lFil, iFil = unpack('<5B', rdr.read(5))
            t2d = Texture2D(s_class, img, bcol, blend, wrpS, wrpT, lFil, iFil)
            rdr.close()
            return t2d
        elif objtype == 255:
            uri = rdr.read().rstrip(b'\x00').decode('utf-8')
            rdr.close()
            return ExternalReference(uri)

        rdr.close()
        return ObjTypeNames[objtype]

    def ReadObjects(self, data):
        rdr = BytesIO(data)
        while True:
            objectHeader = rdr.read(5)
            if objectHeader == b'':
                break
            objectType, sz = unpack('<BI', objectHeader)
            print(f'Got object of type {ObjTypeNames[objectType]}')
            self.objects.append(self.ParseObject(objectType, rdr.read(sz)))
        rdr.close()

    def ReadSections(self):
        while True:
            sectionHeader = self.file.read(9)
            if sectionHeader == b'':
                break
            print(f'Section data starting at {self.file.tell()}')
            compression, totalLen, uncomp = unpack('<BII', sectionHeader)
            sectionLength = totalLen - 13
            self.ReadObjects(self.file.read(sectionLength))
            self.file.read(4)


start = timeit.default_timer()

a = Loader('../testfiles/vrally/car_subaru.m3g')
# a = Loader('/home/zi/tmp/ug/car_exotic.m3g')

print(f'Loaded file in {timeit.default_timer()-start} seconds')

print('Found the following objects in file:')
for o in a.objects:
    print(f'  {o}')
