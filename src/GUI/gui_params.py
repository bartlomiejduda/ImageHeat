"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from typing import Optional

from src.Image.constants import (
    DEFAULT_ROTATE_NAME,
    DEFAULT_ZOOM_NAME,
    DEFAULT_ZOOM_RESAMPLING_NAME,
)


class GuiParams:
    def __init__(self):
        # image parameters
        self.pixel_format: Optional[str] = None
        self.endianess_type: Optional[str] = None
        self.swizzling_type: Optional[str] = None
        self.compression_type: Optional[str] = None
        self.img_start_offset: int = 0
        self.img_end_offset: int = 0
        self.total_file_size: int = 0
        self.img_width: Optional[int] = None
        self.img_height: Optional[int] = None
        self.img_file_path: Optional[str] = None
        self.img_file_name: Optional[str] = None

        # palette parameters
        self.palette_loadfrom_value: Optional[int] = None
        self.palette_file_path: Optional[str] = None
        self.palette_offset: Optional[int] = None
        self.palette_endianess: Optional[str] = None
        self.palette_ps2_swizzle_flag: Optional[bool] = None

        # post-processing
        self.zoom_name: str = DEFAULT_ZOOM_NAME
        self.zoom_resampling_name: str = DEFAULT_ZOOM_RESAMPLING_NAME
        self.vertical_flip_flag: bool = False
        self.horizontal_flip_flag: bool = False
        self.rotate_name: str = DEFAULT_ROTATE_NAME
