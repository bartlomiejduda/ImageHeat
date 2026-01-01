"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import time
from typing import Optional

from reversebox.common.logger import get_logger
from reversebox.image.swizzling.swizzle_ps2 import unswizzle_ps2_palette

from src.GUI.gui_params import GuiParams

logger = get_logger(__name__)

# fmt: off


class HeatPalette:
    def __init__(self, gui_params: GuiParams):
        self.gui_params: GuiParams = gui_params
        self.loaded_palette_data: Optional[bytes] = None
        self.encoded_palette_data: Optional[bytes] = None
        self.decoded_palette_data: Optional[bytes] = None
        self.is_data_loaded_from_palette_file: bool = False
        self.MAX_PALETTE_SIZE: int = 2048

    def _palette_read(self) -> bool:
        # load from the same file
        if not self.is_data_loaded_from_palette_file and self.gui_params.palette_loadfrom_value == 1:
            logger.info("Reading palette data from the same file")
            palette_file = open(self.gui_params.img_file_path, "rb")
            self.loaded_palette_data = palette_file.read()
            palette_file.close()
            self.encoded_palette_data = self.loaded_palette_data
            self.is_data_loaded_from_palette_file = True
        # load from another file
        elif not self.is_data_loaded_from_palette_file and self.gui_params.palette_loadfrom_value == 2:
            logger.info("Reading palette data from the another file")
            palette_file = open(self.gui_params.palette_file_path, "rb")
            self.loaded_palette_data = palette_file.read()
            palette_file.close()
            self.encoded_palette_data = self.loaded_palette_data
            self.is_data_loaded_from_palette_file = True
        else:
            self.encoded_palette_data = self.loaded_palette_data[self.gui_params.palette_offset: self.gui_params.palette_offset + self.MAX_PALETTE_SIZE]

        return True

    def _palette_decode(self) -> bool:
        logger.info("Palette decode start...")

        # calculate end offset
        if len(self.loaded_palette_data) - self.gui_params.palette_offset > self.MAX_PALETTE_SIZE:
            palette_end_offset = self.gui_params.palette_offset + self.MAX_PALETTE_SIZE
        else:
            palette_end_offset = len(self.loaded_palette_data)

        # set initial (encoded) palette data
        encoded_palette_data: bytes = self.encoded_palette_data[self.gui_params.palette_offset:palette_end_offset]

        # unswizzle palette
        if self.gui_params.palette_ps2_swizzle_flag:
            self.decoded_palette_data = unswizzle_ps2_palette(palette_data=encoded_palette_data,
                                                              bpp=16 if len(encoded_palette_data) < 1024 else 32)
        else:
            self.decoded_palette_data = encoded_palette_data  # no decoding needed

        # fill small palette logic
        if len(self.decoded_palette_data) < self.MAX_PALETTE_SIZE:
            new_palette: bytearray = bytearray(self.MAX_PALETTE_SIZE)
            for i in range(self.MAX_PALETTE_SIZE):
                if i < len(self.decoded_palette_data):
                    new_palette[i] = self.decoded_palette_data[i]
                else:
                    new_palette[i] = 0
            self.decoded_palette_data = new_palette

        return True

    def palette_reload(self) -> bool:
        logger.info("Palette reload start")
        start_time = time.time()
        self._palette_read()
        self._palette_decode()
        execution_time = time.time() - start_time
        logger.info(f"Palette reload for pixel_format={self.gui_params.pixel_format} finished successfully. Time: {round(execution_time, 2)} seconds.")
        return True
