"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import enum

PIXEL_FORMATS = [
    "DXT1",
    "RGB565",
    "YUY2",
]


class SupportedPixelFormats(enum.Enum):
    DXT1 = "DXT1"


SWIZZLING_TYPES = [
    "None",
    "PSP Swizzling",
    "XBOX/PS3 Swizzling (Morton Order)",
]
