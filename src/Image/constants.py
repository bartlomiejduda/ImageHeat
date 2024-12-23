"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from dataclasses import dataclass

from reversebox.image.image_formats import ImageFormats


@dataclass
class PixelFormat:
    format_name: str
    format_type: ImageFormats


@dataclass
class SwizzlingType:
    display_name: str
    unique_id: str


@dataclass
class CompressionType:
    display_name: str
    unique_id: str


@dataclass
class EndianessType:
    display_name: str
    unique_id: str


@dataclass
class ZoomType:
    display_name: str
    zoom_value: float


@dataclass
class RotateType:
    display_name: str
    unique_id: str


SUPPORTED_PIXEL_FORMATS: list[PixelFormat] = [
    PixelFormat(format_name=image_format.name, format_type=image_format) for image_format in ImageFormats
]

SUPPORTED_SWIZZLING_TYPES: list[SwizzlingType] = [
    SwizzlingType(display_name="None", unique_id="none"),
    SwizzlingType(display_name="PSP", unique_id="psp"),
    SwizzlingType(display_name="XBOX / PS3 (Morton)", unique_id="morton"),
    SwizzlingType(display_name="Dreamcast / PS Vita", unique_id="dreamcast_psvita"),
    SwizzlingType(display_name="PS4 (Morton)", unique_id="ps4"),
    SwizzlingType(display_name="GameCube / WII", unique_id="gamecube_wii"),
    SwizzlingType(display_name="XBOX 360", unique_id="x360"),
    SwizzlingType(display_name="PS2", unique_id="ps2"),
    SwizzlingType(display_name="PS2 (EA 4-bit)", unique_id="ps2_ea_4bit"),
    SwizzlingType(display_name="BC", unique_id="bc"),
    SwizzlingType(display_name="3DS", unique_id="3ds"),
]

SUPPORTED_COMPRESSION_TYPES: list[CompressionType] = [
    CompressionType(display_name="None", unique_id="none"),
    CompressionType(display_name="TGA RLE", unique_id="rle_tga"),
    CompressionType(display_name="PackBits", unique_id="packbits"),  # Macintosh RLE
]

SUPPORTED_ENDIANESS_TYPES: list[EndianessType] = [
    EndianessType(display_name="Little Endian", unique_id="little"),
    EndianessType(display_name="Big Endian", unique_id="big"),
]

SUPPORTED_ZOOM_TYPES: list[ZoomType] = [
    ZoomType(display_name="0.1x", zoom_value=0.1),
    ZoomType(display_name="0.25x", zoom_value=0.25),
    ZoomType(display_name="0.5x", zoom_value=0.5),
    ZoomType(display_name="1x", zoom_value=1.0),
    ZoomType(display_name="2x", zoom_value=2.0),
    ZoomType(display_name="4x", zoom_value=4.0),
    ZoomType(display_name="8x", zoom_value=8.0),
    ZoomType(display_name="16x", zoom_value=16.0),
]


SUPPORTED_ROTATE_TYPES: list[RotateType] = [
    RotateType(display_name="None", unique_id="none"),
    RotateType(display_name="Rotate 90 Left", unique_id="rotate_90_left"),
    RotateType(display_name="Rotate 90 Right", unique_id="rotate_90_right"),
    RotateType(display_name="Rotate 180", unique_id="rotate_180"),
]


def check_unique_ids(list_to_check: list) -> bool:
    id_list: list = []
    for entry in list_to_check:
        if entry.unique_id in id_list:
            raise Exception(f"ID={entry.unique_id} is not unique!")
        id_list.append(entry.unique_id)
    return True


def get_endianess_id(endianess_name: str) -> str:
    for endianess_type in SUPPORTED_ENDIANESS_TYPES:
        if endianess_name == endianess_type.display_name:
            return endianess_type.unique_id

    raise Exception(f"Couldn't find code for endianess name: {endianess_name}")


def get_swizzling_id(swizzling_name: str) -> str:
    for swizzling_type in SUPPORTED_SWIZZLING_TYPES:
        if swizzling_name == swizzling_type.display_name:
            return swizzling_type.unique_id

    raise Exception(f"Couldn't find code for swizzling name: {swizzling_name}")


def get_compression_id(compression_name: str) -> str:
    for compression_type in SUPPORTED_COMPRESSION_TYPES:
        if compression_name == compression_type.display_name:
            return compression_type.unique_id

    raise Exception(f"Couldn't find code for compression name: {compression_name}")


def get_zoom_value(zoom_name: str) -> float:
    for zoom_type in SUPPORTED_ZOOM_TYPES:
        if zoom_name == zoom_type.display_name:
            return zoom_type.zoom_value

    raise Exception(f"Couldn't find code for zoom name: {zoom_name}")


def get_rotate_id(rotate_name: str) -> str:
    for rotate_type in SUPPORTED_ROTATE_TYPES:
        if rotate_name == rotate_type.display_name:
            return rotate_type.unique_id

    raise Exception(f"Couldn't find code for rotate name: {rotate_name}")


check_unique_ids(SUPPORTED_SWIZZLING_TYPES)
check_unique_ids(SUPPORTED_COMPRESSION_TYPES)
check_unique_ids(SUPPORTED_ENDIANESS_TYPES)
check_unique_ids(SUPPORTED_ROTATE_TYPES)

PIXEL_FORMATS_NAMES: list = [pixel_format.format_name for pixel_format in SUPPORTED_PIXEL_FORMATS]
SWIZZLING_TYPES_NAMES: list = [swizzling_type.display_name for swizzling_type in SUPPORTED_SWIZZLING_TYPES]
COMPRESSION_TYPES_NAMES: list = [compression_type.display_name for compression_type in SUPPORTED_COMPRESSION_TYPES]
ENDIANESS_TYPES_NAMES: list = [endianess_type.display_name for endianess_type in SUPPORTED_ENDIANESS_TYPES]
ZOOM_TYPES_NAMES: list = [zoom_type.display_name for zoom_type in SUPPORTED_ZOOM_TYPES]
ROTATE_TYPES_NAMES: list = [rotate_type.display_name for rotate_type in SUPPORTED_ROTATE_TYPES]
PALETTE_FORMATS_NAMES: list = ["pal", "gst"]

DEFAULT_PIXEL_FORMAT_NAME: str = "RGB565"
DEFAULT_ENDIANESS_NAME: str = ENDIANESS_TYPES_NAMES[0]
DEFAULT_SWIZZLING_NAME: str = SWIZZLING_TYPES_NAMES[0]
DEFAULT_COMPRESSION_NAME: str = COMPRESSION_TYPES_NAMES[0]
DEFAULT_ZOOM_NAME: str = "1x"
DEFAULT_ROTATE_NAME: str = ROTATE_TYPES_NAMES[0]
