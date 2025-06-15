"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import time
from typing import Optional

from reversebox.common.logger import get_logger
from reversebox.image.byte_swap import swap_byte_order_gamecube, swap_byte_order_x360
from reversebox.image.common import (
    calculate_aligned_value,
    get_block_data_size,
    get_bpp_for_image_format,
)
from reversebox.image.compression.compression_packbits import decompress_packbits
from reversebox.image.compression.compression_rle_executioners import (
    decompress_rle_executioners,
)
from reversebox.image.compression.compression_rle_tga import decompress_rle_tga
from reversebox.image.compression.compression_zlib import decompress_zlib
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.swizzling.swizzle_3ds import unswizzle_3ds
from reversebox.image.swizzling.swizzle_bc import unswizzle_bc
from reversebox.image.swizzling.swizzle_gamecube import unswizzle_gamecube
from reversebox.image.swizzling.swizzle_morton import unswizzle_morton
from reversebox.image.swizzling.swizzle_morton_ps4 import unswizzle_ps4
from reversebox.image.swizzling.swizzle_ps2 import unswizzle_ps2
from reversebox.image.swizzling.swizzle_psp import unswizzle_psp
from reversebox.image.swizzling.swizzle_psvita_dreamcast import (
    unswizzle_psvita_dreamcast,
)
from reversebox.image.swizzling.swizzle_switch import unswizzle_switch
from reversebox.image.swizzling.swizzle_wii_u import unswizzle_wii_u
from reversebox.image.swizzling.swizzle_x360 import unswizzle_x360

from src.GUI.gui_params import GuiParams
from src.Image.constants import (
    PIXEL_FORMATS_NAMES,
    get_compression_id,
    get_endianess_id,
    get_swizzling_id,
)
from src.Image.heatpalette import HeatPalette

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
        self.heat_palette: Optional[HeatPalette] = None

    def _image_read(self) -> bool:
        if not self.is_data_loaded_from_file:
            logger.info("Reading image data from file")
            img_file = open(self.gui_params.img_file_path, "rb")
            self.loaded_image_data = img_file.read()
            img_file.close()
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
        palette_format: ImageFormats = self._get_image_format_from_str(self.gui_params.palette_format)

        # endianess logic
        endianess_id: str = get_endianess_id(self.gui_params.endianess_type)

        if endianess_id == "byte_swap_x360":
            endianess_id = "little"
            try:
                self.encoded_image_data = swap_byte_order_x360(self.encoded_image_data)
            except Exception as error:
                logger.warning(f"Byte swap function failed! Error: {error}")

        if endianess_id == "byte_swap_gamecube":
            endianess_id = "little"
            try:
                self.encoded_image_data = swap_byte_order_gamecube(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height)
            except Exception as error:
                logger.warning(f"Byte swap function failed! Error: {error}")

        # image bpp logic
        try:
            image_bpp: int = get_bpp_for_image_format(image_format)
        except Exception as error:
            logger.warning(f"Couldn't get image bpp! Setting default value! Error: {error}")
            image_bpp = 8

        # decompression logic
        compression_id = get_compression_id(self.gui_params.compression_type)
        if compression_id == "none":
            pass
        elif compression_id == "rle_tga":
            self.encoded_image_data = decompress_rle_tga(self.encoded_image_data, image_bpp)
        elif compression_id == "packbits":
            self.encoded_image_data = decompress_packbits(self.encoded_image_data)
        elif compression_id == "zlib":
            self.encoded_image_data = decompress_zlib(self.encoded_image_data)
        elif compression_id == "rle_executioners":
            self.encoded_image_data = decompress_rle_executioners(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        else:
            logger.error(f"Compression type not supported! Type: {compression_id}")

        # unswizzling logic
        swizzling_id = get_swizzling_id(self.gui_params.swizzling_type)
        encoded_data_size: int = len(self.encoded_image_data)

        if swizzling_id == "none":
            pass
        elif swizzling_id == "psp":
            self.encoded_image_data = unswizzle_psp(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "morton":
            self.encoded_image_data = unswizzle_morton(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, block_width_height=1)
        elif swizzling_id == "morton_4x4":
            self.encoded_image_data = unswizzle_morton(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, block_width_height=4)
        elif swizzling_id == "morton_8x8":
            self.encoded_image_data = unswizzle_morton(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, block_width_height=8)
        elif swizzling_id == "dreamcast_psvita":
            self.encoded_image_data = unswizzle_psvita_dreamcast(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, block_width_height=1)
        elif swizzling_id == "dreamcast_psvita_4x4":
            self.encoded_image_data = unswizzle_psvita_dreamcast(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, block_width_height=4)
        elif swizzling_id == "dreamcast_psvita_8x8":
            self.encoded_image_data = unswizzle_psvita_dreamcast(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, block_width_height=8)
        elif swizzling_id == "ps4":
            self.encoded_image_data = unswizzle_ps4(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, block_width=4, block_height=4, block_data_size=get_block_data_size(image_format))
        elif swizzling_id == "ps4_padding":
            self.gui_params.img_width = calculate_aligned_value(self.gui_params.img_width, 32)
            self.gui_params.img_height = calculate_aligned_value(self.gui_params.img_height, 32)
            self.encoded_image_data = unswizzle_ps4(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, block_width=4, block_height=4, block_data_size=get_block_data_size(image_format))
        elif swizzling_id == "nintendo_switch_4_4":
            self.encoded_image_data = unswizzle_switch(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, bytes_per_block=4, block_height=4)
        elif swizzling_id == "nintendo_switch_4_8":
            self.encoded_image_data = unswizzle_switch(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, bytes_per_block=4, block_height=8)
        elif swizzling_id == "nintendo_switch_1_16":
            self.encoded_image_data = unswizzle_switch(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, bytes_per_block=1, block_height=16)
        elif swizzling_id == "gamecube_wii":
            self.encoded_image_data = unswizzle_gamecube(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        elif swizzling_id == "x360_1_1":  # 8-bpp
            self.encoded_image_data = unswizzle_x360(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height,
                                                     block_pixel_size=1, texel_byte_pitch=1)
        elif swizzling_id == "x360_1_2":  # 16-bpp
            self.encoded_image_data = unswizzle_x360(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height,
                                                     block_pixel_size=1, texel_byte_pitch=2)
        elif swizzling_id == "x360_1_4":  # 32-bpp
            self.encoded_image_data = unswizzle_x360(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height,
                                                     block_pixel_size=1, texel_byte_pitch=4)
        elif swizzling_id == "x360_4_8":  # 64-bit 4x4 blocks
            self.encoded_image_data = unswizzle_x360(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height,
                                                     block_pixel_size=4, texel_byte_pitch=8)
        elif swizzling_id == "x360_4_16":  # 128-bit 4x4 blocks, used in MT Framework
            self.encoded_image_data = unswizzle_x360(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height,
                                                     block_pixel_size=4, texel_byte_pitch=16)
        elif swizzling_id == "ps2_type1":
            self.encoded_image_data = unswizzle_ps2(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, swizzle_type=1)
        elif swizzling_id == "ps2_type2":
            self.encoded_image_data = unswizzle_ps2(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, swizzle_type=2)
        elif swizzling_id == "ps2_type3":
            self.encoded_image_data = unswizzle_ps2(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp, swizzle_type=3)
        elif swizzling_id == "wii_u_linear":
            self.encoded_image_data = unswizzle_wii_u(self.gui_params.img_width, self.gui_params.img_height, image_format=0x0000001a,
                                                      tile_mode=0, swizzle_type=0, pitch=64, input_data=self.encoded_image_data)
        elif swizzling_id == "wii_u_bc":
            self.encoded_image_data = unswizzle_wii_u(self.gui_params.img_width, self.gui_params.img_height, image_format=0x00000031,
                                                      tile_mode=4, swizzle_type=0, pitch=64, input_data=self.encoded_image_data)
        elif swizzling_id == "bc":
            self.encoded_image_data = unswizzle_bc(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, 8, 8, image_bpp)
        elif swizzling_id == "3ds":
            self.encoded_image_data = unswizzle_3ds(self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_bpp)
        else:
            logger.error(f"Swizzling type not supported! Type: {swizzling_id}")

        if len(self.encoded_image_data) != encoded_data_size:
            logger.warning(f"Different data size after unswizzling! Swizzling_id: {swizzling_id}")

        # decoding logic
        if image_format in (ImageFormats.RGB121,

                            ImageFormats.RGBX2222,
                            ImageFormats.RGBA2222,
                            ImageFormats.RGB121_BYTE,
                            ImageFormats.RGB332,
                            ImageFormats.BGR332,
                            ImageFormats.GRAY8,
                            ImageFormats.ALPHA8,
                            ImageFormats.LA44,
                            ImageFormats.R8,
                            ImageFormats.G8,
                            ImageFormats.B8,

                            ImageFormats.GRAY8A,
                            ImageFormats.GRAY16,
                            ImageFormats.RG88,
                            ImageFormats.RGB565,
                            ImageFormats.BGR565,
                            ImageFormats.RGBX5551,
                            ImageFormats.RGBA5551,
                            ImageFormats.RGBT5551,
                            ImageFormats.BGRA5551,
                            ImageFormats.BGRX5551,
                            ImageFormats.RGBA4444,
                            ImageFormats.ARGB4444,
                            ImageFormats.XRGB4444,
                            ImageFormats.ABGR4444,
                            ImageFormats.XBGR4444,
                            ImageFormats.RGBX4444,
                            ImageFormats.BGRA4444,
                            ImageFormats.BGRX4444,
                            ImageFormats.XRGB1555,
                            ImageFormats.XBGR1555,
                            ImageFormats.ARGB1555,
                            ImageFormats.ABGR1555,
                            ImageFormats.R16,
                            ImageFormats.G16,
                            ImageFormats.B16,

                            ImageFormats.RGB888,
                            ImageFormats.BGR888,

                            ImageFormats.RGBA8888,
                            ImageFormats.BGRA8888,
                            ImageFormats.ARGB8888,
                            ImageFormats.ABGR8888,
                            ImageFormats.XRGB8888,
                            ImageFormats.RGBX8888,
                            ImageFormats.BGRX8888,
                            ImageFormats.RGBM8888,
                            ImageFormats.R32,
                            ImageFormats.G32,
                            ImageFormats.B32,

                            ImageFormats.RGB48,
                            ImageFormats.BGR48,

                            ImageFormats.N64_RGB5A3,
                            ImageFormats.N64_I4,
                            ImageFormats.N64_I8,
                            ImageFormats.N64_IA4,
                            ImageFormats.N64_IA8
                            ):
            self.decoded_image_data = image_decoder.decode_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format, endianess_id
            )
        elif image_format in (ImageFormats.PAL4,
                              ImageFormats.PAL8,
                              ImageFormats.PAL16,
                              ImageFormats.PAL32,
                              ImageFormats.PAL_I8A8
                              ):

            if (self.gui_params.palette_loadfrom_value == 1 and self.gui_params.img_file_path is not None) \
             or (self.gui_params.palette_loadfrom_value == 2 and self.gui_params.palette_file_path is not None):  # noqa: E121
                palette_endianess_id: str = get_endianess_id(self.gui_params.palette_endianess)
                self.heat_palette = HeatPalette(self.gui_params)
                self.heat_palette.palette_reload()

                self.decoded_image_data = image_decoder.decode_indexed_image(
                    self.encoded_image_data, self.heat_palette.decoded_palette_data, self.gui_params.img_width, self.gui_params.img_height,
                    image_format, palette_format, endianess_id, palette_endianess_id
                )
            else:
                logger.info("Palette not loaded...")

        elif image_format in (ImageFormats.N64_RGBA32, ImageFormats.N64_CMPR):
            self.decoded_image_data = image_decoder.decode_n64_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        elif image_format in (ImageFormats.BC1_DXT1,
                              ImageFormats.BC2_DXT3,
                              ImageFormats.BC3_DXT5,
                              ImageFormats.BC4_UNORM,
                              ImageFormats.BC5_UNORM,
                              ImageFormats.BC6H_SF16,
                              ImageFormats.BC6H_UF16,
                              ImageFormats.BC7_UNORM
                              ):
            self.decoded_image_data = image_decoder.decode_compressed_image(
                self.encoded_image_data, self.gui_params.img_width, self.gui_params.img_height, image_format
            )
        elif "ASTC" in image_format.value\
                or "PVRTCI" in image_format.value\
                or "ETC" in image_format.value\
                or "EAC" in image_format.value\
                or image_format in (ImageFormats.DXT2, ImageFormats.DXT4, ImageFormats.BW1bpp,
                                    ImageFormats.SharedExponentR9G9B9E5, ImageFormats.RGBG8888, ImageFormats.GRGB8888,
                                    ImageFormats.RGBM, ImageFormats.RGBD):
            self.decoded_image_data = image_decoder.decode_pvrtexlib_image(
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
                              ImageFormats.YUV444P,
                              ImageFormats.AYUV):
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
