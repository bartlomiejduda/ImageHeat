"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
from typing import Optional

from reversebox.common.logger import get_logger

from src.GUI.gui_params import GuiParams

logger = get_logger(__name__)


class HeatImage:
    def __init__(self, gui_params: GuiParams):
        self.gui_params: GuiParams = gui_params
        self.encoded_image_data: Optional[bytes] = None
        self.decoded_image_data: Optional[bytes] = None

    def image_read(self) -> bool:
        img_file = open(self.gui_params.img_file_path, "rb")
        img_file.seek(self.gui_params.img_start_offset)
        data_size: int = self.gui_params.img_end_offset - self.gui_params.img_start_offset
        self.encoded_image_data = img_file.read(data_size)
        return True

    def image_decode(self) -> bool:
        logger.info("Image decode start...")
        # if self.gui_params.pixel_format not in SupportedPixelFormats:
        #     raise Exception("Not supported pixel format!")

        self.decoded_image_data = self.encoded_image_data  # TODO
        return True

    def image_reload(self) -> bool:
        logger.info("Image reload start")
        self.image_read()
        self.image_decode()
        logger.info("Image reload finished successfully")
        return True
