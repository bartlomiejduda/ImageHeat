"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from PIL.Image import Resampling
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
class ZoomResamplingType:
    display_name: str
    unique_id: str
    type: Resampling


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
    CompressionType(display_name="ZLIB (Deflate)", unique_id="zlib"),
    CompressionType(display_name="Executioners RLE", unique_id="rle_executioners"),
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

SUPPORTED_ZOOM_RESAMPLING_TYPES: list[ZoomResamplingType] = [
    ZoomResamplingType(display_name="Nearest", unique_id="nearest", type=Resampling.NEAREST),
    ZoomResamplingType(display_name="Box", unique_id="box", type=Resampling.BOX),
    ZoomResamplingType(display_name="Bilinear", unique_id="bilinear", type=Resampling.BILINEAR),
    ZoomResamplingType(display_name="Hamming", unique_id="hamming", type=Resampling.HAMMING),
    ZoomResamplingType(display_name="Bicubic", unique_id="bicubic", type=Resampling.BICUBIC),
    ZoomResamplingType(display_name="Lanczos", unique_id="lanczos", type=Resampling.LANCZOS),
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


def get_resampling_type(zoom_resampling_name: str) -> Resampling:
    for zoom_resampling_type in SUPPORTED_ZOOM_RESAMPLING_TYPES:
        if zoom_resampling_name == zoom_resampling_type.display_name:
            return zoom_resampling_type.type

    raise Exception(f"Couldn't find code for zoom resampling name: {zoom_resampling_name}")


def get_rotate_id(rotate_name: str) -> str:
    for rotate_type in SUPPORTED_ROTATE_TYPES:
        if rotate_name == rotate_type.display_name:
            return rotate_type.unique_id

    raise Exception(f"Couldn't find code for rotate name: {rotate_name}")


check_unique_ids(SUPPORTED_SWIZZLING_TYPES)
check_unique_ids(SUPPORTED_COMPRESSION_TYPES)
check_unique_ids(SUPPORTED_ENDIANESS_TYPES)
check_unique_ids(SUPPORTED_ROTATE_TYPES)
check_unique_ids(SUPPORTED_ZOOM_RESAMPLING_TYPES)

PIXEL_FORMATS_NAMES: list = [pixel_format.format_name for pixel_format in SUPPORTED_PIXEL_FORMATS]
SWIZZLING_TYPES_NAMES: list = [swizzling_type.display_name for swizzling_type in SUPPORTED_SWIZZLING_TYPES]
COMPRESSION_TYPES_NAMES: list = [compression_type.display_name for compression_type in SUPPORTED_COMPRESSION_TYPES]
ENDIANESS_TYPES_NAMES: list = [endianess_type.display_name for endianess_type in SUPPORTED_ENDIANESS_TYPES]
ZOOM_TYPES_NAMES: list = [zoom_type.display_name for zoom_type in SUPPORTED_ZOOM_TYPES]
ZOOM_RESAMPLING_TYPES_NAMES: list = [
    zoom_resampling_type.display_name for zoom_resampling_type in SUPPORTED_ZOOM_RESAMPLING_TYPES
]
ROTATE_TYPES_NAMES: list = [rotate_type.display_name for rotate_type in SUPPORTED_ROTATE_TYPES]
PALETTE_FORMATS_NAMES: list = ["pal", "gst"]

DEFAULT_PIXEL_FORMAT_NAME: str = "RGB565"
DEFAULT_ENDIANESS_NAME: str = ENDIANESS_TYPES_NAMES[0]
DEFAULT_SWIZZLING_NAME: str = SWIZZLING_TYPES_NAMES[0]
DEFAULT_COMPRESSION_NAME: str = COMPRESSION_TYPES_NAMES[0]
DEFAULT_ZOOM_NAME: str = "1x"
DEFAULT_ZOOM_RESAMPLING_NAME: str = ZOOM_RESAMPLING_TYPES_NAMES[0]
DEFAULT_ROTATE_NAME: str = ROTATE_TYPES_NAMES[0]


class TranslationKeys(str, Enum):
    TRANSLATION_TEXT_IMAGE_PARAMETERS = "TRANSLATION_TEXT_IMAGE_PARAMETERS"
    TRANSLATION_TEXT_IMAGE_WIDTH = "TRANSLATION_TEXT_IMAGE_WIDTH"
    TRANSLATION_TEXT_IMAGE_HEIGHT = "TRANSLATION_TEXT_IMAGE_HEIGHT"
    TRANSLATION_TEXT_START_OFFSET = "TRANSLATION_TEXT_START_OFFSET"
    TRANSLATION_TEXT_END_OFFSET = "TRANSLATION_TEXT_END_OFFSET"
    TRANSLATION_TEXT_PIXEL_FORMAT = "TRANSLATION_TEXT_PIXEL_FORMAT"
    TRANSLATION_TEXT_ENDIANESS_TYPE = "TRANSLATION_TEXT_ENDIANESS_TYPE"
    TRANSLATION_TEXT_SWIZZLING_TYPE = "TRANSLATION_TEXT_SWIZZLING_TYPE"
    TRANSLATION_TEXT_COMPRESSION_TYPE = "TRANSLATION_TEXT_COMPRESSION_TYPE"

    TRANSLATION_TEXT_PALETTE_PARAMETERS = "TRANSLATION_TEXT_PALETTE_PARAMETERS"
    TRANSLATION_TEXT_LOAD_FROM = "TRANSLATION_TEXT_LOAD_FROM"
    TRANSLATION_TEXT_SAME_FILE = "TRANSLATION_TEXT_SAME_FILE"
    TRANSLATION_TEXT_ANOTHER_FILE = "TRANSLATION_TEXT_ANOTHER_FILE"
    TRANSLATION_TEXT_PALETTE_FILE = "TRANSLATION_TEXT_PALETTE_FILE"
    TRANSLATION_TEXT_BROWSE = "TRANSLATION_TEXT_BROWSE"
    TRANSLATION_TEXT_PAL_OFFSET = "TRANSLATION_TEXT_PAL_OFFSET"
    TRANSLATION_TEXT_PALETTE_ENDIANESS = "TRANSLATION_TEXT_PALETTE_ENDIANESS"
    TRANSLATION_TEXT_PS2_PALETTE_SWIZZLE = "TRANSLATION_TEXT_PS2_PALETTE_SWIZZLE"

    TRANSLATION_TEXT_IMAGE_PREVIEW = "TRANSLATION_TEXT_IMAGE_PREVIEW"

    TRANSLATION_TEXT_INFO_LABELFRAME = "TRANSLATION_TEXT_INFO_LABELFRAME"
    TRANSLATION_TEXT_INFO_FILENAME_LABEL = "TRANSLATION_TEXT_INFO_FILENAME_LABEL"
    TRANSLATION_TEXT_INFO_FILE_SIZE = "TRANSLATION_TEXT_INFO_FILE_SIZE"
    TRANSLATION_TEXT_INFO_PIXEL_X = "TRANSLATION_TEXT_INFO_PIXEL_X"
    TRANSLATION_TEXT_INFO_PIXEL_Y = "TRANSLATION_TEXT_INFO_PIXEL_Y"
    TRANSLATION_TEXT_INFO_PIXEL_OFFSET = "TRANSLATION_TEXT_INFO_PIXEL_OFFSET"
    TRANSLATION_TEXT_INFO_PIXEL_VALUE = "TRANSLATION_TEXT_INFO_PIXEL_VALUE"

    TRANSLATION_TEXT_CONTROLS_LABELFRAME = "TRANSLATION_TEXT_CONTROLS_LABELFRAME"

    TRANSLATION_TEXT_CONTROLS_ACTION_IMG_WIDTH = "TRANSLATION_TEXT_CONTROLS_ACTION_IMG_WIDTH"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_WIDTH = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_WIDTH"
    TRANSLATION_TEXT_CONTROLS_ACTION_IMG_HEIGHT = "TRANSLATION_TEXT_CONTROLS_ACTION_IMG_HEIGHT"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_HEIGHT = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_HEIGHT"
    TRANSLATION_TEXT_CONTROLS_ACTION_DOUBLE_HALVE_WIDTH = "TRANSLATION_TEXT_CONTROLS_ACTION_DOUBLE_HALVE_WIDTH"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_DOUBLE_HALVE_WIDTH = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_DOUBLE_HALVE_WIDTH"
    TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_BYTE = "TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_BYTE"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_BYTE = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_BYTE"
    TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_ROW = "TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_ROW"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_ROW = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_ROW"
    TRANSLATION_TEXT_CONTROLS_ACTION_PIXEL_FORMAT = "TRANSLATION_TEXT_CONTROLS_ACTION_PIXEL_FORMAT"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_PIXEL_FORMAT = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_PIXEL_FORMAT"
    TRANSLATION_TEXT_CONTROLS_ACTION_ENDIANESS = "TRANSLATION_TEXT_CONTROLS_ACTION_ENDIANESS"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_ENDIANESS = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_ENDIANESS"
    TRANSLATION_TEXT_CONTROLS_ACTION_SWIZZLING = "TRANSLATION_TEXT_CONTROLS_ACTION_SWIZZLING"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_SWIZZLING = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_SWIZZLING"
    TRANSLATION_TEXT_CONTROLS_ACTION_COMPRESSION = "TRANSLATION_TEXT_CONTROLS_ACTION_COMPRESSION"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_COMPRESSION = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_COMPRESSION"
    TRANSLATION_TEXT_CONTROLS_ACTION_RELOAD_IMG = "TRANSLATION_TEXT_CONTROLS_ACTION_RELOAD_IMG"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_RELOAD_IMG = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_RELOAD_IMG"
    TRANSLATION_TEXT_CONTROLS_ACTION_ZOOM = "TRANSLATION_TEXT_CONTROLS_ACTION_ZOOM"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_ZOOM = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_ZOOM"
    TRANSLATION_TEXT_POST_PROCESSING_LABELFRAME = "TRANSLATION_TEXT_POST_PROCESSING_LABELFRAME"
    TRANSLATION_TEXT_POST_PROCESSING_ZOOM = "TRANSLATION_TEXT_POST_PROCESSING_ZOOM"
    TRANSLATION_TEXT_POST_PROCESSING_RESAMPLING = "TRANSLATION_TEXT_POST_PROCESSING_RESAMPLING"
    TRANSLATION_TEXT_POST_PROCESSING_VERTICAL_FLIP = "TRANSLATION_TEXT_POST_PROCESSING_VERTICAL_FLIP"
    TRANSLATION_TEXT_POST_PROCESSING_HORIZONTAL_FLIP = "TRANSLATION_TEXT_POST_PROCESSING_HORIZONTAL_FLIP"
    TRANSLATION_TEXT_POST_PROCESSING_ROTATE = "TRANSLATION_TEXT_POST_PROCESSING_ROTATE"
    TRANSLATION_TEXT_FILEMENU_OPEN_FILE = "TRANSLATION_TEXT_FILEMENU_OPEN_FILE"
    TRANSLATION_TEXT_FILEMENU_SAVE_AS = "TRANSLATION_TEXT_FILEMENU_SAVE_AS"


@dataclass
class TranslationEntry:
    id: str
    default: str
    text: Optional[str] = None


TRANSLATION_MEMORY: List[TranslationEntry] = [
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_IMAGE_PARAMETERS, default="Image Parameters"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_IMAGE_WIDTH, default="Img Width"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_IMAGE_HEIGHT, default="Img Height"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_START_OFFSET, default="Start Offset (Decimal)"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_END_OFFSET, default="End Offset (Decimal)"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PIXEL_FORMAT, default="Pixel Format"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_ENDIANESS_TYPE, default="Endianess Type"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_SWIZZLING_TYPE, default="Swizzling Type"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_COMPRESSION_TYPE, default="Compression Type"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PALETTE_PARAMETERS, default="Palette Parameters"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_LOAD_FROM, default="Load From"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_SAME_FILE, default="Same File"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_ANOTHER_FILE, default="Another File"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PALETTE_FILE, default="Palette File"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_BROWSE, default="Browse..."),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PAL_OFFSET, default="Pal. Offset"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PALETTE_ENDIANESS, default="Palette Endianess"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PS2_PALETTE_SWIZZLE, default="PS2 Palette Swizzle"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_IMAGE_PREVIEW, default="Image Preview"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_LABELFRAME, default="Info"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_FILENAME_LABEL, default="File Name: "),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_FILE_SIZE, default="File Size: "),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_X, default="Pixel X: "),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_Y, default="Pixel Y: "),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_OFFSET, default="Pixel Offset: "),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE, default="Pixel Value (hex): "),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_LABELFRAME, default="Controls"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_IMG_WIDTH, default="Img Width"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_WIDTH, default="Left/Right"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_IMG_HEIGHT, default="Img Height"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_HEIGHT, default="Up/Down"),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_DOUBLE_HALVE_WIDTH, default="Double/Halve Width"
    ),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_DOUBLE_HALVE_WIDTH, default="Q/W"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_BYTE, default="Step-By-Byte"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_BYTE, default="CTRL+Up/Down"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_ROW, default="Step-By-Row"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_ROW, default="SHIFT+Up/Down"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_PIXEL_FORMAT, default="Pixel Format"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_PIXEL_FORMAT, default="Z/X"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_ENDIANESS, default="Endianess"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_ENDIANESS, default="E"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_SWIZZLING, default="Swizzling"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_SWIZZLING, default="K/L"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_COMPRESSION, default="Compression"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_COMPRESSION, default="O/P"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_RELOAD_IMG, default="Reload Img"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_RELOAD_IMG, default="Enter"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_ZOOM, default="Zoom"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_ZOOM, default="Mouse Wheel"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_LABELFRAME, default="Post-Processing"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_ZOOM, default="Zoom"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_RESAMPLING, default="Resampling"),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_VERTICAL_FLIP, default="Vertical Flip (Top-Down)"
    ),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_HORIZONTAL_FLIP, default="Horizontal Flip (Left-Right)"
    ),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_ROTATE, default="Rotate"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_FILEMENU_OPEN_FILE, default="Open File"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_FILEMENU_SAVE_AS, default="Save As..."),
]
