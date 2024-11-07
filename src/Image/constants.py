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


SUPPORTED_PIXEL_FORMATS: list[PixelFormat] = [
    PixelFormat(format_name=image_format.name, format_type=image_format) for image_format in ImageFormats
]

SUPPORTED_SWIZZLING_TYPES: list[SwizzlingType] = [
    SwizzlingType(display_name="None", unique_id="none"),
    SwizzlingType(display_name="PSP", unique_id="psp"),
    SwizzlingType(display_name="XBOX/PS3 (Morton)", unique_id="morton"),
    SwizzlingType(display_name="Dreamcast (Morton)", unique_id="dreamcast"),
    SwizzlingType(display_name="PS4 (Morton)", unique_id="ps4"),
    SwizzlingType(display_name="BC", unique_id="bc"),
]


def check_swizzling_codes() -> bool:
    swizzling_codes = []
    for swizzling_type in SUPPORTED_SWIZZLING_TYPES:
        if swizzling_type.unique_id in swizzling_codes:
            raise Exception(f"ID={swizzling_type.unique_id} is not unique!")
        swizzling_codes.append(swizzling_type.unique_id)
    return True


def get_swizzling_id(swizzling_name: str) -> str:
    for swizzling_type in SUPPORTED_SWIZZLING_TYPES:
        if swizzling_name == swizzling_type.display_name:
            return swizzling_type.unique_id

    raise Exception(f"Couldn't find code for swizzling name: {swizzling_name}")


check_swizzling_codes()

PIXEL_FORMATS_NAMES: list = [pixel_format.format_name for pixel_format in SUPPORTED_PIXEL_FORMATS]
SWIZZLING_TYPES_NAMES: list = [swizzling_type.display_name for swizzling_type in SUPPORTED_SWIZZLING_TYPES]
