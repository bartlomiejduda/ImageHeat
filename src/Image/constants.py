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
class EndianessType:
    display_name: str
    unique_id: str


SUPPORTED_PIXEL_FORMATS: list[PixelFormat] = [
    PixelFormat(format_name=image_format.name, format_type=image_format) for image_format in ImageFormats
]

SUPPORTED_SWIZZLING_TYPES: list[SwizzlingType] = [
    SwizzlingType(display_name="None", unique_id="none"),
    SwizzlingType(display_name="PSP", unique_id="psp"),
    SwizzlingType(display_name="XBOX/PS3 (Morton)", unique_id="morton"),
    SwizzlingType(display_name="Dreamcast (Morton)", unique_id="dreamcast"),
    SwizzlingType(display_name="PS4 (Morton)", unique_id="ps4"),
    SwizzlingType(display_name="XBOX 360", unique_id="x360"),
    SwizzlingType(display_name="PS2", unique_id="ps2"),
    SwizzlingType(display_name="PS2 (EA 4-bit)", unique_id="ps2_ea_4bit"),
    SwizzlingType(display_name="BC", unique_id="bc"),
]

SUPPORTED_ENDIANESS_TYPES: list[EndianessType] = [
    EndianessType(display_name="Little Endian", unique_id="little"),
    EndianessType(display_name="Big Endian", unique_id="big"),
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


check_unique_ids(SUPPORTED_SWIZZLING_TYPES)
check_unique_ids(SUPPORTED_ENDIANESS_TYPES)

PIXEL_FORMATS_NAMES: list = [pixel_format.format_name for pixel_format in SUPPORTED_PIXEL_FORMATS]
DEFAULT_PIXEL_FORMAT_NAME = "RGB565"
SWIZZLING_TYPES_NAMES: list = [swizzling_type.display_name for swizzling_type in SUPPORTED_SWIZZLING_TYPES]
ENDIANESS_TYPES_NAMES: list = [endianess_type.display_name for endianess_type in SUPPORTED_ENDIANESS_TYPES]
