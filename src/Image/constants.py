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
    PixelFormat(format_name="RGBA8888", format_type=ImageFormats.RGBA8888),
    PixelFormat(format_name="DXT1", format_type=ImageFormats.DXT1),
]

PIXEL_FORMATS_NAMES: list = [pixel_format.format_name for pixel_format in SUPPORTED_PIXEL_FORMATS]


SWIZZLING_TYPES: list = [
    "None",
    "PSP Swizzling",
    "XBOX/PS3 Swizzling (Morton Order)",
]
