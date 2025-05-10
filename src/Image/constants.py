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


EXCLUDED_PIXEL_FORMATS: list[ImageFormats] = [
    ImageFormats.RGB121,
    ImageFormats.RGB121_BYTE,
    ImageFormats.GST121,
    ImageFormats.GST122,
    ImageFormats.GST421,
    ImageFormats.GST422,
    ImageFormats.GST221,
    ImageFormats.GST222,
    ImageFormats.GST821,
    ImageFormats.GST822,
]

SUPPORTED_PIXEL_FORMATS: list[PixelFormat] = [
    PixelFormat(format_name=image_format.name, format_type=image_format)
    for image_format in ImageFormats
    if image_format not in EXCLUDED_PIXEL_FORMATS
]

SUPPORTED_PALETTE_FORMATS: list[ImageFormats] = [
    ImageFormats.RGB565,
    ImageFormats.BGR565,
    ImageFormats.RGBX5551,
    ImageFormats.BGRX5551,
    ImageFormats.XRGB1555,
    ImageFormats.XBGR1555,
    ImageFormats.RGBA4444,
    ImageFormats.RGBX4444,
    ImageFormats.BGRA4444,
    ImageFormats.BGRX4444,
    ImageFormats.ARGB4444,
    ImageFormats.XRGB4444,
    ImageFormats.ABGR4444,
    ImageFormats.XBGR4444,
    ImageFormats.RGB888,
    ImageFormats.BGR888,
    ImageFormats.RGBA8888,
    ImageFormats.RGBX8888,
    ImageFormats.BGRA8888,
    ImageFormats.BGRX8888,
    ImageFormats.ARGB8888,
    ImageFormats.ABGR8888,
    ImageFormats.XRGB8888,
    ImageFormats.N64_I4,
    ImageFormats.N64_I8,
    ImageFormats.N64_IA4,
    ImageFormats.N64_IA8,
    ImageFormats.N64_RGB5A3,
    ImageFormats.GRAY8,
    ImageFormats.GRAY16,
    ImageFormats.GRAY8A,
    ImageFormats.RGBX2222,
]

SUPPORTED_SWIZZLING_TYPES: list[SwizzlingType] = [
    SwizzlingType(display_name="None", unique_id="none"),
    SwizzlingType(display_name="PSP", unique_id="psp"),
    SwizzlingType(display_name="XBOX / PS3 (linear)", unique_id="morton"),
    SwizzlingType(display_name="XBOX / PS3 (4x4)", unique_id="morton_4x4"),
    SwizzlingType(display_name="XBOX / PS3 (8x8)", unique_id="morton_8x8"),
    SwizzlingType(display_name="DC / PS Vita (linear)", unique_id="dreamcast_psvita"),
    SwizzlingType(display_name="DC / PS Vita (4x4)", unique_id="dreamcast_psvita_4x4"),
    SwizzlingType(display_name="DC / PS Vita (8x8)", unique_id="dreamcast_psvita_8x8"),
    SwizzlingType(display_name="PS4 (Morton)", unique_id="ps4"),
    SwizzlingType(display_name="Nintendo Switch (4,8)", unique_id="nintendo_switch_4_8"),
    SwizzlingType(display_name="Nintendo Switch (1,16)", unique_id="nintendo_switch_1_16"),
    SwizzlingType(display_name="GameCube / WII", unique_id="gamecube_wii"),
    SwizzlingType(display_name="XBOX 360 (1, 1)", unique_id="x360_1_1"),
    SwizzlingType(display_name="XBOX 360 (1, 2)", unique_id="x360_1_2"),
    SwizzlingType(display_name="XBOX 360 (1, 4)", unique_id="x360_1_4"),
    SwizzlingType(display_name="XBOX 360 (4, 8)", unique_id="x360_4_8"),
    SwizzlingType(display_name="XBOX 360 (4, 16)", unique_id="x360_4_16"),
    SwizzlingType(display_name="PS2 (Type 1)", unique_id="ps2_type1"),
    SwizzlingType(display_name="PS2 (Type 2)", unique_id="ps2_type2"),
    SwizzlingType(display_name="PS2 (Type 3)", unique_id="ps2_type3"),
    SwizzlingType(display_name="WII U (linear)", unique_id="wii_u_linear"),
    SwizzlingType(display_name="WII U (BC)", unique_id="wii_u_bc"),
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
PALETTE_FORMATS_NAMES: list = [palette_format.value.upper() for palette_format in SUPPORTED_PALETTE_FORMATS]
SWIZZLING_TYPES_NAMES: list = [swizzling_type.display_name for swizzling_type in SUPPORTED_SWIZZLING_TYPES]
COMPRESSION_TYPES_NAMES: list = [compression_type.display_name for compression_type in SUPPORTED_COMPRESSION_TYPES]
ENDIANESS_TYPES_NAMES: list = [endianess_type.display_name for endianess_type in SUPPORTED_ENDIANESS_TYPES]
ZOOM_TYPES_NAMES: list = [zoom_type.display_name for zoom_type in SUPPORTED_ZOOM_TYPES]
ZOOM_RESAMPLING_TYPES_NAMES: list = [
    zoom_resampling_type.display_name for zoom_resampling_type in SUPPORTED_ZOOM_RESAMPLING_TYPES
]
ROTATE_TYPES_NAMES: list = [rotate_type.display_name for rotate_type in SUPPORTED_ROTATE_TYPES]
PALETTE_FORMATS_REGEX_NAMES: list = ["pal", "gst"]

DEFAULT_PIXEL_FORMAT_NAME: str = "RGB565"
DEFAULT_PALETTE_FORMAT_NAME: str = "RGB565"
DEFAULT_ENDIANESS_NAME: str = ENDIANESS_TYPES_NAMES[0]
DEFAULT_SWIZZLING_NAME: str = SWIZZLING_TYPES_NAMES[0]
DEFAULT_COMPRESSION_NAME: str = COMPRESSION_TYPES_NAMES[0]
DEFAULT_ZOOM_NAME: str = "1x"
DEFAULT_ZOOM_RESAMPLING_NAME: str = ZOOM_RESAMPLING_TYPES_NAMES[0]
DEFAULT_ROTATE_NAME: str = ROTATE_TYPES_NAMES[0]


class ConfigKeys(str, Enum):
    SAVE_AS_DIRECTORY_PATH = "save_as_directory_path"
    SAVE_RAW_DATA_DIRECTORY_PATH = "save_raw_data_directory_path"
    OPEN_FILE_DIRECTORY_PATH = "open_file_directory_path"
    OPEN_PALETTE_DIRECTORY_PATH = "open_palette_directory_path"
    CURRENT_PROGRAM_LANGUAGE = "current_program_language"
    CURRENT_CANVAS_COLOR = "current_canvas_color"


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
    TRANSLATION_TEXT_PAL_FORMAT = "TRANSLATION_TEXT_PAL_FORMAT"
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
    TRANSLATION_TEXT_CONTROLS_ACTION_PALETTE_FORMAT = "TRANSLATION_TEXT_CONTROLS_ACTION_PALETTE_FORMAT"
    TRANSLATION_TEXT_CONTROLS_SHORTCUT_PALETTE_FORMAT = "TRANSLATION_TEXT_CONTROLS_SHORTCUT_PALETTE_FORMAT"
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
    TRANSLATION_TEXT_FILEMENU_SAVE_RAW_DATA = "TRANSLATION_TEXT_FILEMENU_SAVE_RAW_DATA"
    TRANSLATION_TEXT_FILEMENU_QUIT = "TRANSLATION_TEXT_FILEMENU_QUIT"
    TRANSLATION_TEXT_FILEMENU_FILE = "TRANSLATION_TEXT_FILEMENU_FILE"
    TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE = "TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE"
    TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_EN = "TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_EN"
    TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_PL = "TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_PL"
    TRANSLATION_TEXT_OPTIONSMENU_OPTIONS = "TRANSLATION_TEXT_OPTIONSMENU_OPTIONS"
    TRANSLATION_TEXT_HELPMENU_ABOUT = "TRANSLATION_TEXT_HELPMENU_ABOUT"
    TRANSLATION_TEXT_HELPMENU_HELP = "TRANSLATION_TEXT_HELPMENU_HELP"
    TRANSLATION_TEXT_ABOUT_WINDOW_TITLE = "TRANSLATION_TEXT_ABOUT_WINDOW_TITLE"
    TRANSLATION_TEXT_ABOUT_WINDOW_VERSION = "TRANSLATION_TEXT_ABOUT_WINDOW_VERSION"
    TRANSLATION_TEXT_ABOUT_WINDOW_COPYRIGHT = "TRANSLATION_TEXT_ABOUT_WINDOW_COPYRIGHT"
    TRANSLATION_TEXT_EXPORT_FILETYPES_DDS = "TRANSLATION_TEXT_EXPORT_FILETYPES_DDS"
    TRANSLATION_TEXT_EXPORT_FILETYPES_PNG = "TRANSLATION_TEXT_EXPORT_FILETYPES_PNG"
    TRANSLATION_TEXT_EXPORT_FILETYPES_BMP = "TRANSLATION_TEXT_EXPORT_FILETYPES_BMP"
    TRANSLATION_TEXT_EXPORT_FILETYPES_BINARY = "TRANSLATION_TEXT_EXPORT_FILETYPES_BINARY"
    TRANSLATION_TEXT_POPUPS_FAILED_TO_OPEN_FILE = "TRANSLATION_TEXT_POPUPS_FAILED_TO_OPEN_FILE"
    TRANSLATION_TEXT_POPUPS_FAILED_TO_SAVE_FILE = "TRANSLATION_TEXT_POPUPS_FAILED_TO_SAVE_FILE"
    TRANSLATION_TEXT_POPUPS_EMPTY_IMAGE_DATA = "TRANSLATION_TEXT_POPUPS_EMPTY_IMAGE_DATA"
    TRANSLATION_TEXT_POPUPS_FILE_SAVED_SUCCESSFULLY = "TRANSLATION_TEXT_POPUPS_FILE_SAVED_SUCCESSFULLY"
    TRANSLATION_TEXT_POPUPS_RAW_DATA_SAVED_SUCCESSFULLY = "TRANSLATION_TEXT_POPUPS_RAW_DATA_SAVED_SUCCESSFULLY"
    TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_COLOR = "TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_COLOR"
    TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_GRAY = "TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_GRAY"
    TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_BLACK = "TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_BLACK"
    TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_WHITE = "TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_WHITE"


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
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_PAL_FORMAT, default="Palette Format"),
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
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_PALETTE_FORMAT, default="Palette Format"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_PALETTE_FORMAT, default="N/M"),
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
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_FILEMENU_SAVE_RAW_DATA, default="Save Raw Data"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_FILEMENU_QUIT, default="Quit"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_FILEMENU_FILE, default="File"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE, default="Language"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_EN, default="English (Default)"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_PL, default="Polish"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_OPTIONS, default="Options"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_HELPMENU_ABOUT, default="About..."),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_HELPMENU_HELP, default="Help"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_ABOUT_WINDOW_TITLE, default="About ImageHeat"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_ABOUT_WINDOW_VERSION, default="Version: "),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_ABOUT_WINDOW_COPYRIGHT,
        default="Copyright 2024-2025 © Bartlomiej Duda. All Rights Reserved.\nFor the latest version visit ImageHeat Github page at\n",
    ),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_DDS, default="DDS files"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_PNG, default="PNG files"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_BMP, default="BMP files"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_BINARY, default="Binary files"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_POPUPS_FAILED_TO_OPEN_FILE, default="Failed to open file!"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_POPUPS_FAILED_TO_SAVE_FILE, default="Failed to save file!"),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_POPUPS_EMPTY_IMAGE_DATA, default="Empty image data! Export not possible!"
    ),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_POPUPS_FILE_SAVED_SUCCESSFULLY, default="File saved successfully!"
    ),
    TranslationEntry(
        id=TranslationKeys.TRANSLATION_TEXT_POPUPS_RAW_DATA_SAVED_SUCCESSFULLY, default="Raw data saved successfully!"
    ),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_COLOR, default="Canvas Color"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_GRAY, default="Gray (Default)"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_BLACK, default="Black"),
    TranslationEntry(id=TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_WHITE, default="White"),
]
