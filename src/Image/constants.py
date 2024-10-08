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


SUPPORTED_PIXEL_FORMATS: list[PixelFormat] = [
    PixelFormat(format_name=image_format.name, format_type=image_format) for image_format in ImageFormats
]

PIXEL_FORMATS_NAMES: list = [pixel_format.format_name for pixel_format in SUPPORTED_PIXEL_FORMATS]


SWIZZLING_TYPES: list = ["None", "PSP", "XBOX/PS3 (Morton)", "Dreamcast", "BC"]
