"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from typing import Optional


class GuiParams:
    def __init__(self):
        self.pixel_format: Optional[str] = None
        self.swizzling_type: Optional[str] = None
        self.img_start_offset: int = 0
        self.img_end_offset: int = 0
        self.total_file_size: int = 0
        self.img_width: Optional[int] = None
        self.img_height: Optional[int] = None
        self.img_file_path: Optional[str] = None
        self.img_file_name: Optional[str] = None
