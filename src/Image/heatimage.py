"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import time
from typing import Optional

from reversebox.common.logger import get_logger
from reversebox.image.common import get_bpp_for_image_format
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.swizzling.swizzle_bc import unswizzle_bc
from reversebox.image.swizzling.swizzle_morton import unswizzle_morton
from reversebox.image.swizzling.swizzle_morton_dreamcast import (
    unswizzle_morton_dreamcast,
)
from reversebox.image.swizzling.swizzle_morton_ps4 import unswizzle_ps4
from reversebox.image.swizzling.swizzle_ps2 import unswizzle_ps2, unswizzle_ps2_ea_4bit
from reversebox.image.swizzling.swizzle_psp import unswizzle_psp
from reversebox.image.swizzling.swizzle_x360 import unswizzle_x360

from src.GUI.gui_params import GuiParams
from src.Image.constants import PIXEL_FORMATS_NAMES, get_swizzling_id

logger = get_logger(__name__)

# fmt: off


class HeatImage:
    def __init__(self, gui_params: GuiParams):
        self.gui_params: GuiParams = gui_params
        self.loaded_image_data: Optional[bytes] = None
        self.encoded_image_data: Optional[bytes] = None
        self.decoded_image_data: Optional[bytes] = None
        self.is_preview_error: bool = False
        self.is_data_loaded_from_file: bool = False

    def _image_read(self) -> bool:
        if not self.is_data_loaded_from_file:
            logger.info("Reading image data from file")
            img_file = open(self.gui_params.img_file_path, "rb")
            self.loaded_image_data = img_file.read()
            self.encoded_image_data = self.loaded_image_data
            self.is_data_loaded_from_file = True
        else:
            self.encoded_image_data = self.loaded_image_data[self.gui_params.img_start_offset: self.gui_params.img_end_offset]

        return True

    def _get_image_format_from_str(self, pixel_format: str) -> ImageFormats:
        return ImageFormats[pixel_format]

    def _image_decode(self) -> bool:
        logger.info("Image decode start...")
        if self.gui_params.pixel_format not in PIXEL_FORMATS_NAMES:
            logger.error("[1] Not supported pixel format!")
            self.is_preview_error = True

        image_decoder = ImageDecoder()
        image_format: ImageFormats = self._get_image_format_from_str(self.gui_params.pixel_format)

        # unswizzling logic
        swizzling_id = get_swizzling_id(self.gui_params.swizzling_type)

        try:
            image_bpp: int = get_bpp_for_image_format(image_format)
        except Exception as error:
            logger.warning(f"Couldn't get image bpp! Setting default value! Error: {error}")
            image_bpp = 8

        if swizzling_id == "none":
            pass
        elif swizzling_id == "psp":
            self.encoded_image_data = unswizzle_psp(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "morton":
            self.encoded_image_data = unswizzle_morton(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "dreamcast":
            self.encoded_image_data = unswizzle_morton_dreamcast(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "ps4":
            self.encoded_image_data = unswizzle_ps4(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "x360":
            self.encoded_image_data = unswizzle_x360(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "ps2":
            self.encoded_image_data = unswizzle_ps2(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "ps2_ea_4bit":
            if image_bpp == 4:
                self.encoded_image_data = unswizzle_ps2_ea_4bit(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "bc":
            self.encoded_image_data = unswizzle_bc(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, 8, 8, image_bpp)
        else:
            logger.error(f"Swizzling type not supported! Type: {swizzling_id}")

        if image_format in (ImageFormats.RGB121,

                            ImageFormats.RGBX2222,
                            ImageFormats.RGBA2222,
                            ImageFormats.RGB121_BYTE,
                            ImageFormats.RGB332,
                            ImageFormats.BGR332,
                            ImageFormats.GRAY8,

                            ImageFormats.GRAY8A,
                            ImageFormats.GRAY16,
                            ImageFormats.RGB565,
                            ImageFormats.BGR565,
                            ImageFormats.RGBX5551,
                            ImageFormats.RGBA5551,
                            ImageFormats.ARGB4444,
                            ImageFormats.RGBA4444,
                            ImageFormats.RGBX4444,
                            ImageFormats.BGRX4444,
                            ImageFormats.XRGB1555,
                            ImageFormats.XBGR1555,
                            ImageFormats.ARGB1555,
                            ImageFormats.ABGR1555,

                            ImageFormats.RGB888,
                            ImageFormats.BGR888,

                            ImageFormats.RGBA8888,
                            ImageFormats.BGRA8888,
                            ImageFormats.ARGB8888,
                            ImageFormats.ABGR8888,
                            ImageFormats.XRGB8888,
                            ImageFormats.RGBX8888,
                            ImageFormats.XBGR8888,
                            ImageFormats.BGRX8888,

                            ImageFormats.RGB48,
                            ImageFormats.BGR48,

                            ImageFormats.N64_RGB5A3,
                            ImageFormats.N64_I4,
                            ImageFormats.N64_I8,
                            ImageFormats.N64_IA4,
                            ImageFormats.N64_IA8
                            ):
            self.decoded_image_data = image_decoder.decode_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        elif image_format in (ImageFormats.N64_RGBA32, ImageFormats.N64_CMPR):
            self.decoded_image_data = image_decoder.decode_n64_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        elif image_format in (ImageFormats.DXT1, ImageFormats.DXT3, ImageFormats.DXT5):
            self.decoded_image_data = image_decoder.decode_compressed_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        elif image_format in (ImageFormats.GST121,
                              ImageFormats.GST221,
                              ImageFormats.GST421,
                              ImageFormats.GST821,
                              ImageFormats.GST122,
                              ImageFormats.GST222,
                              ImageFormats.GST422,
                              ImageFormats.GST822):
            logger.error("[2] Not supported pixel format!")
            self.is_preview_error = True
        elif image_format in (ImageFormats.YUV410P,
                              ImageFormats.YUV411P,
                              ImageFormats.YUV411_UYYVYY411,
                              ImageFormats.YUV420_NV12,
                              ImageFormats.YUV420_NV21,
                              ImageFormats.YUV420P,
                              ImageFormats.YUVA420P,
                              ImageFormats.YUV422P,
                              ImageFormats.YUV422_UYVY,
                              ImageFormats.YUV422_YUY2,
                              ImageFormats.YUV440P,
                              ImageFormats.YUV444P):
            self.decoded_image_data = image_decoder.decode_yuv_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        elif image_format == ImageFormats.BUMPMAP_SR:
            self.decoded_image_data = image_decoder.decode_bumpmap_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        else:
            logger.error("[3] Not supported pixel format!")
            self.is_preview_error = True

        return True

    def image_reload(self) -> bool:
        logger.info("Image reload start")
        start_time = time.time()
        self.is_preview_error = False
        self._image_read()
        self._image_decode()
        execution_time = time.time() - start_time
        logger.info(f"Image reload for pixel_format={self.gui_params.pixel_format} finished successfully. Time: {round(execution_time, 2)} seconds.")
        return True
