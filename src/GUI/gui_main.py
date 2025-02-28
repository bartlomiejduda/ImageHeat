"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import json
import math
import os
import platform
import sys
import time
import tkinter as tk
from configparser import ConfigParser
from idlelib.tooltip import Hovertip
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

from PIL import Image, ImageTk
from PIL.Image import Transpose
from reversebox.common.common import (
    convert_bytes_to_hex_string,
    convert_from_bytes_to_mb_string,
    get_file_extension_uppercase,
)
from reversebox.common.logger import get_logger
from reversebox.image.common import (
    convert_bpp_to_bytes_per_pixel,
    convert_bpp_to_bytes_per_pixel_float,
    get_bpp_for_image_format,
    is_compressed_image_format,
)
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper
from tkhtmlview import HTMLLabel

from src.GUI.about_window import AboutWindow
from src.GUI.gui_params import GuiParams
from src.Image.constants import (
    COMPRESSION_TYPES_NAMES,
    DEFAULT_COMPRESSION_NAME,
    DEFAULT_ENDIANESS_NAME,
    DEFAULT_PALETTE_FORMAT_NAME,
    DEFAULT_PIXEL_FORMAT_NAME,
    DEFAULT_ROTATE_NAME,
    DEFAULT_SWIZZLING_NAME,
    DEFAULT_ZOOM_NAME,
    DEFAULT_ZOOM_RESAMPLING_NAME,
    ENDIANESS_TYPES_NAMES,
    PALETTE_FORMATS_NAMES,
    PALETTE_FORMATS_REGEX_NAMES,
    PIXEL_FORMATS_NAMES,
    ROTATE_TYPES_NAMES,
    SWIZZLING_TYPES_NAMES,
    TRANSLATION_MEMORY,
    ZOOM_RESAMPLING_TYPES_NAMES,
    ZOOM_TYPES_NAMES,
    ConfigKeys,
    TranslationEntry,
    TranslationKeys,
    get_compression_id,
    get_resampling_type,
    get_rotate_id,
    get_zoom_value,
)
from src.Image.heatimage import HeatImage

# default app settings
WINDOW_HEIGHT = 575
WINDOW_WIDTH = 1000

logger = get_logger(__name__)

# fmt: off


class ImageHeatGUI:
    def __init__(self, master: tk.Tk, in_version_num: str, in_main_directory: str):
        logger.info("GUI init...")
        self.master = master
        self.VERSION_NUM = in_version_num
        self.MAIN_DIRECTORY = in_main_directory
        self.TRANSLATION_MEMORY = TRANSLATION_MEMORY
        master.title(f"ImageHeat {in_version_num}")
        master.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        if platform.uname().system == "Linux":
            icon_filename = "heat_icon.png"
        else:
            icon_filename = "heat_icon.ico"
        self.icon_path = os.path.join(self.MAIN_DIRECTORY, "data", "img", icon_filename)
        self.preview_image_path = os.path.join(self.MAIN_DIRECTORY, "data", "img", "preview_not_supported.png")
        self.gui_font = ('Arial', 8)
        self.opened_image: Optional[HeatImage] = None
        self.gui_params: GuiParams = GuiParams()
        self.preview_instance = None
        self.ph_img = None
        self.preview_final_pil_image = None
        self.validate_spinbox_command = (master.register(self.validate_spinbox), '%P')
        self.pixel_x: int = 1
        self.pixel_y: int = 1
        self.pixel_offset: int = 0
        self.pixel_value_str: str = ""
        self.pixel_value_rgba: bytearray = bytearray(10)

        # icon logic
        try:
            if platform.uname().system == "Linux":
                self.master.iconphoto(False, tk.PhotoImage(file=self.icon_path))
            else:
                self.master.iconbitmap(self.icon_path)
        except tk.TclError:
            logger.info("Can't load the icon file from %s", self.icon_path)

        # user config logic
        self.user_config = ConfigParser()
        self.user_config_file_name: str = "config.ini"
        self.user_config.add_section("config")
        self.user_config.set("config", ConfigKeys.SAVE_AS_DIRECTORY_PATH, "")
        self.user_config.set("config", ConfigKeys.SAVE_RAW_DATA_DIRECTORY_PATH, "")
        self.user_config.set("config", ConfigKeys.OPEN_FILE_DIRECTORY_PATH, "")
        self.user_config.set("config", ConfigKeys.OPEN_PALETTE_DIRECTORY_PATH, "")
        self.user_config.set("config", ConfigKeys.CURRENT_PROGRAM_LANGUAGE, "EN")
        self.user_config.set("config", ConfigKeys.CURRENT_CANVAS_COLOR, "#595959")
        if not os.path.exists(self.user_config_file_name):
            with open(self.user_config_file_name, "w") as configfile:
                self.user_config.write(configfile)

        self.user_config.read(self.user_config_file_name)
        try:
            self.current_save_as_directory_path = self.user_config.get("config", ConfigKeys.SAVE_AS_DIRECTORY_PATH)
            self.current_save_raw_data_directory_path = self.user_config.get("config", ConfigKeys.SAVE_RAW_DATA_DIRECTORY_PATH)
            self.current_open_file_directory_path = self.user_config.get("config", ConfigKeys.OPEN_FILE_DIRECTORY_PATH)
            self.current_open_palette_directory_path = self.user_config.get("config", ConfigKeys.OPEN_PALETTE_DIRECTORY_PATH)
            self.current_program_language = tk.StringVar(value=self.user_config.get("config", ConfigKeys.CURRENT_PROGRAM_LANGUAGE))
            self.current_background_color = tk.StringVar(value=self.user_config.get("config", ConfigKeys.CURRENT_CANVAS_COLOR))
        except Exception as error:
            logger.error(f"Error while loading user config: {error}")
            self.current_save_as_directory_path = ""
            self.current_save_raw_data_directory_path = ""
            self.current_open_file_directory_path = ""
            self.current_open_palette_directory_path = ""
            self.current_program_language = tk.StringVar(value="EN")
            self.current_background_color = tk.StringVar(value="#595959")

        ########################
        # MAIN FRAME           #
        ########################
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        ########################
        # IMAGE PARAMETERS BOX #
        ########################
        self.parameters_labelframe = tk.LabelFrame(self.main_frame, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_PARAMETERS), font=self.gui_font)
        self.parameters_labelframe.place(x=5, y=5, width=160, height=340)

        ###################################
        # IMAGE PARAMETERS - IMAGE WIDTH  #
        ###################################
        self.width_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_WIDTH), anchor="w", font=self.gui_font)
        self.width_label.place(x=5, y=5, width=70, height=20)

        self.current_width = tk.StringVar(value="0")
        self.width_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_width, from_=0, to=sys.maxsize,
                                        command=self.gui_reload_image_on_gui_element_change)
        self.width_spinbox.place(x=5, y=25, width=70, height=20)
        self.width_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _decrease_image_width_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            self.width_spinbox.invoke("buttondown")
            self.master.focus()

        def _increase_image_width_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            self.width_spinbox.invoke("buttonup")
            self.master.focus()

        def _halve_width_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            curr_width: int = 1
            try:
                curr_width = int(self.current_width.get())
                if curr_width == 0:
                    curr_width += 1
            except Exception:
                pass

            self.current_width.set(str(curr_width // 2))
            self.reload_image_callback(event)
            self.master.focus()

        def _double_width_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            curr_width: int = 1
            try:
                curr_width = int(self.current_width.get())
                if curr_width == 0:
                    curr_width += 1
            except Exception:
                pass
            self.current_width.set(str(curr_width * 2))
            self.reload_image_callback(event)
            self.master.focus()

        self.master.bind("<Left>", _decrease_image_width_by_shortcut)
        self.master.bind("<Right>", _increase_image_width_by_shortcut)

        self.master.bind("<q>", _halve_width_by_shortcut)
        self.master.bind("<w>", _double_width_by_shortcut)

        ######################################
        # IMAGE PARAMETERS - IMAGE HEIGHT    #
        ######################################
        self.height_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_HEIGHT), anchor="w", font=self.gui_font)
        self.height_label.place(x=85, y=5, width=65, height=20)

        self.current_height = tk.StringVar(value="0")
        self.height_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_height, from_=0, to=sys.maxsize,
                                         command=self.gui_reload_image_on_gui_element_change)
        self.height_spinbox.place(x=85, y=25, width=65, height=20)
        self.height_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _decrease_image_height_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            self.height_spinbox.invoke("buttondown")
            self.master.focus()

        def _increase_image_height_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            self.height_spinbox.invoke("buttonup")
            self.master.focus()

        self.master.bind("<Up>", _decrease_image_height_by_shortcut)
        self.master.bind("<Down>", _increase_image_height_by_shortcut)


        ###########################################
        # IMAGE PARAMETERS - IMAGE START OFFSET   #
        ###########################################
        self.img_start_offset_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_START_OFFSET), anchor="w", font=self.gui_font)
        self.img_start_offset_label.place(x=5, y=50, width=145, height=20)

        self.current_start_offset = tk.StringVar(value="0")
        self.img_start_offset_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_start_offset, from_=0, to=sys.maxsize,
                                                   command=self.gui_reload_image_on_gui_element_change)
        self.img_start_offset_spinbox.place(x=5, y=70, width=145, height=20)
        self.img_start_offset_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _step_up_by_byte_by_shortcut(event):  # decrease offsets by byte
            curr_start_offset: int = 0
            curr_end_offset: int = 0
            try:
                curr_start_offset = int(self.current_start_offset.get())
                curr_end_offset = int(self.current_end_offset.get())
            except Exception:
                pass
            if curr_start_offset <= curr_end_offset:
                self.img_start_offset_spinbox.invoke("buttondown")
                self.master.focus()

        def _step_down_by_byte_by_shortcut(event):  # increase offsets by byte
            curr_start_offset: int = 0
            curr_end_offset: int = 0
            try:
                curr_start_offset = int(self.current_start_offset.get())
                curr_end_offset = int(self.current_end_offset.get())
            except Exception:
                pass

            if curr_start_offset <= curr_end_offset:
                self.img_start_offset_spinbox.invoke("buttonup")
                if curr_end_offset <= self.gui_params.total_file_size:
                    self.img_end_offset_spinbox.invoke("buttonup")
                self.master.focus()

        def _step_down_by_row_by_shortcut(event):  # increase offsets by row
            if event.state & 4:
                return  # skip CTRL

            curr_start_offset: int = 0
            curr_end_offset: int = 0
            curr_width: int = 1
            current_pixel_format: str = self.pixel_format_combobox.get()
            image_format: ImageFormats = ImageFormats[current_pixel_format]
            bpp: int = get_bpp_for_image_format(image_format)
            bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
            try:
                curr_start_offset = int(self.current_start_offset.get())
                curr_end_offset = int(self.current_end_offset.get())
                curr_width = int(self.current_width.get())
            except Exception:
                pass
            row_size: int = curr_width * bytes_per_pixel
            new_start_offset: int = curr_start_offset + row_size
            new_end_offset: int = curr_end_offset + row_size
            if new_start_offset <= self.gui_params.total_file_size:
                self.current_start_offset.set(str(new_start_offset))
                if new_end_offset <= self.gui_params.total_file_size:
                    self.current_end_offset.set(str(new_end_offset))
                self.reload_image_callback(event)
                self.master.focus()

        def _step_up_by_row_by_shortcut(event):  # decrease offsets by row
            if event.state & 4:
                return  # skip CTRL

            curr_start_offset: int = 0
            curr_width: int = 1
            current_pixel_format: str = self.pixel_format_combobox.get()
            image_format: ImageFormats = ImageFormats[current_pixel_format]
            bpp: int = get_bpp_for_image_format(image_format)
            bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
            try:
                curr_start_offset = int(self.current_start_offset.get())
                curr_width = int(self.current_width.get())
            except Exception:
                pass
            row_size: int = curr_width * bytes_per_pixel
            new_start_offset: int = curr_start_offset - row_size
            if new_start_offset >= 0:
                self.current_start_offset.set(str(new_start_offset))
                self.reload_image_callback(event)
                self.master.focus()

        self.master.bind("<Control-Up>", _step_up_by_byte_by_shortcut)
        self.master.bind("<Control-Down>", _step_down_by_byte_by_shortcut)

        self.master.bind("<Shift-Up>", _step_up_by_row_by_shortcut)
        self.master.bind("<Shift-Down>", _step_down_by_row_by_shortcut)

        ##########################################
        # IMAGE PARAMETERS - IMAGE END OFFSET    #
        ##########################################
        self.img_end_offset_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_END_OFFSET), anchor="w", font=self.gui_font)
        self.img_end_offset_label.place(x=5, y=90, width=145, height=20)

        self.current_end_offset = tk.StringVar(value="0")
        self.img_end_offset_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_end_offset, from_=0, to=sys.maxsize,
                                                 command=self.gui_reload_image_on_gui_element_change)
        self.img_end_offset_spinbox.place(x=5, y=110, width=145, height=20)
        self.img_end_offset_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        ####################################
        # IMAGE PARAMETERS - PIXEL FORMAT  #
        ####################################

        self.pixel_format_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PIXEL_FORMAT), anchor="w", font=self.gui_font)
        self.pixel_format_label.place(x=5, y=135, width=145, height=20)

        self.pixel_format_combobox = ttk.Combobox(self.parameters_labelframe,
                                                  values=PIXEL_FORMATS_NAMES, font=self.gui_font, state='readonly')
        self.pixel_format_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.pixel_format_combobox.place(x=5, y=155, width=145, height=20)
        self.pixel_format_combobox.set(DEFAULT_PIXEL_FORMAT_NAME)

        def _get_previous_pixel_format_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.pixel_format_combobox.current()
            last = len(self.pixel_format_combobox['values']) - 1
            try:
                self.pixel_format_combobox.current(selection - 1)
            except tk.TclError:
                self.pixel_format_combobox.current(last)
            self.reload_image_callback(event)

        def _get_next_pixel_format_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.pixel_format_combobox.current()
            try:
                self.pixel_format_combobox.current(selection + 1)
            except tk.TclError:
                self.pixel_format_combobox.current(0)
            self.reload_image_callback(event)

        self.master.bind("<z>", _get_previous_pixel_format_by_key)
        self.master.bind("<x>", _get_next_pixel_format_by_key)

        ####################################
        # IMAGE PARAMETERS - ENDIANESS     #
        ####################################

        self.endianess_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_ENDIANESS_TYPE), anchor="w", font=self.gui_font)
        self.endianess_label.place(x=5, y=180, width=145, height=20)

        self.current_endianess = tk.StringVar(value="none")
        self.endianess_combobox = ttk.Combobox(self.parameters_labelframe, values=ENDIANESS_TYPES_NAMES, textvariable=self.current_endianess,
                                               font=self.gui_font, state='readonly')
        self.endianess_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.endianess_combobox.place(x=5, y=200, width=145, height=20)
        self.endianess_combobox.set(DEFAULT_ENDIANESS_NAME)

        def _get_next_endianess_type_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.endianess_combobox.current()
            try:
                self.endianess_combobox.current(selection + 1)
            except tk.TclError:
                self.endianess_combobox.current(0)
            self.reload_image_callback(event)

        self.master.bind("<e>", _get_next_endianess_type_by_key)


        ####################################
        # IMAGE PARAMETERS - SWIZZLING     #
        ####################################
        self.swizzling_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_SWIZZLING_TYPE), anchor="w", font=self.gui_font)
        self.swizzling_label.place(x=5, y=225, width=145, height=20)

        self.current_swizzling = tk.StringVar(value="none")
        self.swizzling_combobox = ttk.Combobox(self.parameters_labelframe,
                                               values=SWIZZLING_TYPES_NAMES, textvariable=self.current_swizzling, font=self.gui_font, state='readonly')
        self.swizzling_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.swizzling_combobox.place(x=5, y=245, width=145, height=20)
        self.swizzling_combobox.set(DEFAULT_SWIZZLING_NAME)

        def _get_previous_swizzling_type_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.swizzling_combobox.current()
            last = len(self.swizzling_combobox['values']) - 1
            try:
                self.swizzling_combobox.current(selection - 1)
            except tk.TclError:
                self.swizzling_combobox.current(last)
            self.reload_image_callback(event)

        def _get_next_swizzling_type_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.swizzling_combobox.current()
            try:
                self.swizzling_combobox.current(selection + 1)
            except tk.TclError:
                self.swizzling_combobox.current(0)
            self.reload_image_callback(event)

        self.master.bind("<k>", _get_previous_swizzling_type_by_key)
        self.master.bind("<l>", _get_next_swizzling_type_by_key)

        ####################################
        # IMAGE PARAMETERS - COMPRESSION     #
        ####################################
        self.compression_label = tk.Label(self.parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_COMPRESSION_TYPE), anchor="w", font=self.gui_font)
        self.compression_label.place(x=5, y=270, width=145, height=20)

        self.current_compression = tk.StringVar(value="none")
        self.compression_combobox = ttk.Combobox(self.parameters_labelframe, values=COMPRESSION_TYPES_NAMES, textvariable=self.current_compression, font=self.gui_font, state='readonly')
        self.compression_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.compression_combobox.place(x=5, y=290, width=145, height=20)
        self.compression_combobox.set(DEFAULT_COMPRESSION_NAME)

        def _get_previous_compression_type_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.compression_combobox.current()
            last = len(self.compression_combobox['values']) - 1
            try:
                self.compression_combobox.current(selection - 1)
            except tk.TclError:
                self.compression_combobox.current(last)
            self.reload_image_callback(event)

        def _get_next_compression_type_by_key(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.compression_combobox.current()
            try:
                self.compression_combobox.current(selection + 1)
            except tk.TclError:
                self.compression_combobox.current(0)
            self.reload_image_callback(event)

        self.master.bind("<o>", _get_previous_compression_type_by_key)
        self.master.bind("<p>", _get_next_compression_type_by_key)



        ###########################
        # PALETTE PARAMETERS BOX  #
        ###########################
        self.palette_parameters_labelframe = tk.LabelFrame(self.main_frame, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PALETTE_PARAMETERS), font=self.gui_font)
        self.palette_parameters_labelframe.place(x=5, y=345, width=160, height=225)


        ########################################
        # PALETTE PARAMETERS BOX  - LOAD FROM  #
        ########################################
        self.palette_load_from_label = tk.Label(self.palette_parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_LOAD_FROM), anchor="w", font=self.gui_font)
        self.palette_load_from_label.place(x=5, y=0, width=60, height=20)

        self.palette_load_from_variable = tk.IntVar(value=1)

        self.palette_load_from_same_file_radio_button = tk.Radiobutton(self.palette_parameters_labelframe,
                                                                       text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_SAME_FILE), variable=self.palette_load_from_variable,
                                                                       value=1, command=self.gui_reload_image_on_gui_element_change,
                                                                       anchor="w", font=self.gui_font)
        self.palette_load_from_same_file_radio_button.place(x=65, y=0, width=90, height=20)
        self.palette_load_from_same_file_radio_button.select()

        self.palette_load_from_another_file_radio_button = tk.Radiobutton(self.palette_parameters_labelframe,
                                                                          text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_ANOTHER_FILE),
                                                                          variable=self.palette_load_from_variable,
                                                                          value=2, command=self.gui_reload_image_on_gui_element_change,
                                                                          anchor="w", font=self.gui_font)
        self.palette_load_from_another_file_radio_button.place(x=65, y=15, width=90, height=20)

        self.palette_palfile_label = tk.Label(self.palette_parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PALETTE_FILE), anchor="w",
                                              font=self.gui_font)
        self.palette_palfile_label.place(x=5, y=40, width=60, height=20)

        self.palette_palfile_button = tk.Button(self.palette_parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_BROWSE),
                                                command=self.open_palette_file, font=self.gui_font)
        self.palette_palfile_button.place(x=70, y=40, width=80, height=20)

        ###########################################
        # PALETTE PARAMETERS BOX  - PAL FORMAT  #
        ###########################################

        self.palette_palformat_label = tk.Label(self.palette_parameters_labelframe, text=self.get_translation_text(
            TranslationKeys.TRANSLATION_TEXT_PAL_FORMAT), anchor="w", font=self.gui_font)
        self.palette_palformat_label.place(x=5, y=65, width=90, height=20)

        self.palette_current_palformat = tk.StringVar(value="none")
        self.palette_format_combobox = ttk.Combobox(self.palette_parameters_labelframe, values=PALETTE_FORMATS_NAMES, textvariable=self.palette_current_palformat,
                                                    font=self.gui_font, state='readonly')
        self.palette_format_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.palette_format_combobox.place(x=5, y=85, width=145, height=20)
        self.palette_format_combobox.set(DEFAULT_PALETTE_FORMAT_NAME)

        ###########################################
        # PALETTE PARAMETERS BOX  - PAL OFFSET  #
        ###########################################

        self.palette_paloffset_label = tk.Label(self.palette_parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PAL_OFFSET), anchor="w",
                                                font=self.gui_font)
        self.palette_paloffset_label.place(x=5, y=115, width=60, height=20)

        self.palette_current_paloffset = tk.StringVar(value="0")
        self.palette_paloffset_spinbox = tk.Spinbox(self.palette_parameters_labelframe, textvariable=self.palette_current_paloffset, from_=0, to=sys.maxsize,
                                                    command=self.gui_reload_image_on_gui_element_change)
        self.palette_paloffset_spinbox.place(x=75, y=115, width=75, height=20)
        self.palette_paloffset_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        #################################################
        # PALETTE PARAMETERS BOX  - PALETTE ENDIANESS   #
        #################################################

        self.palette_endianess_label = tk.Label(self.palette_parameters_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PALETTE_ENDIANESS), anchor="w", font=self.gui_font)
        self.palette_endianess_label.place(x=5, y=140, width=100, height=20)

        self.palette_current_endianess = tk.StringVar(value="none")
        self.palette_endianess_combobox = ttk.Combobox(self.palette_parameters_labelframe, values=ENDIANESS_TYPES_NAMES, textvariable=self.palette_current_endianess,
                                                       font=self.gui_font, state='readonly')
        self.palette_endianess_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.palette_endianess_combobox.place(x=5, y=160, width=145, height=20)
        self.palette_endianess_combobox.set(DEFAULT_ENDIANESS_NAME)

        ###########################################
        # PALETTE PARAMETERS BOX  - PS2 SWIZZLE   #
        ###########################################

        self.palette_ps2swizzle_variable = tk.StringVar(value="OFF")
        self.palette_ps2swizzle_checkbutton = tk.Checkbutton(self.palette_parameters_labelframe,
                                                             text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PS2_PALETTE_SWIZZLE),
                                                             variable=self.palette_ps2swizzle_variable,
                                                             anchor="w", onvalue="ON", offvalue="OFF",
                                                             font=self.gui_font, command=self.gui_reload_image_on_gui_element_change)
        self.palette_ps2swizzle_checkbutton.place(x=5, y=185, width=140, height=20)


        #####################################################
        # PALETTE PARAMETERS BOX  - INITIAL DISABLE LOGIC   #
        #####################################################

        self.parameters_box_disable_enable_logic()

        ##########################
        # FORCE RELOAD #
        ##########################

        def _force_reload_image_by_pressing_enter(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            self.reload_image_callback(event)

        self.master.bind("<Return>", _force_reload_image_by_pressing_enter)

        ##########################
        # INFO BOX #
        ##########################

        self.info_labelframe = tk.LabelFrame(self.main_frame, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_LABELFRAME), font=self.gui_font)
        self.info_labelframe.place(x=-200, y=5, width=195, height=145, relx=1)

        self.infobox_file_name_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILENAME_LABEL), ""), wrap=None)
        self.infobox_file_name_tooltip = Hovertip(self.infobox_file_name_label, self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILENAME_LABEL))
        self.infobox_file_name_label.place(x=5, y=5, width=185, height=18)

        self.infobox_file_size_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILE_SIZE), ""), wrap=None)
        self.infobox_file_size_label.place(x=5, y=25, width=175, height=18)

        self.infobox_pixel_x_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_X), ""), wrap=None)
        self.infobox_pixel_x_label.place(x=5, y=45, width=175, height=18)

        self.infobox_pixel_y_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_Y), ""), wrap=None)
        self.infobox_pixel_y_label.place(x=5, y=65, width=175, height=18)

        self.infobox_pixel_offset_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_OFFSET), ""), wrap=None)
        self.infobox_pixel_offset_label.place(x=5, y=85, width=175, height=18)

        self.infobox_pixel_value_hex_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE), ""), wrap=None)
        self.infobox_pixel_value_hex_label.place(x=5, y=105, width=175, height=18)

        ##########################
        # CONTROLS BOX #
        ##########################

        self.controls_labelframe = tk.LabelFrame(self.main_frame, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_LABELFRAME), font=self.gui_font)
        self.controls_labelframe.place(x=-200, y=150, width=195, height=185, relx=1)

        self.controls_all_info_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_controls_label(), wrap=None)
        self.controls_all_info_label.place(x=5, y=5, width=185, height=160)

        ##########################
        # POST-PROCESSING BOX #
        ##########################

        self.postprocessing_labelframe = tk.LabelFrame(self.main_frame, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_LABELFRAME), font=self.gui_font)
        self.postprocessing_labelframe.place(x=-200, y=335, width=195, height=150, relx=1)

        # zoom
        self.postprocessing_zoom_label = tk.Label(self.postprocessing_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_ZOOM), anchor="w", font=self.gui_font)
        self.postprocessing_zoom_label.place(x=5, y=5, width=60, height=20)

        self.postprocessing_zoom_combobox = ttk.Combobox(self.postprocessing_labelframe, values=ZOOM_TYPES_NAMES, font=self.gui_font, state='readonly')
        self.postprocessing_zoom_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.postprocessing_zoom_combobox.place(x=45, y=5, width=70, height=20)
        self.postprocessing_zoom_combobox.set(DEFAULT_ZOOM_NAME)

        def _zoom_by_shortcut(event):
            if event.state & 5:
                return  # skip SHIFT or CTRL

            selection = self.postprocessing_zoom_combobox.current()
            if event.delta > 0:  # zoom in
                try:
                    self.postprocessing_zoom_combobox.current(selection + 1)
                except tk.TclError:
                    pass
            else:  # zoom out
                try:
                    self.postprocessing_zoom_combobox.current(selection - 1)
                except tk.TclError:
                    pass
            self.reload_image_callback(event)

        self.master.bind("<MouseWheel>", _zoom_by_shortcut)

        # zoom resampling
        self.postprocessing_zoom_resampling_label = tk.Label(self.postprocessing_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_RESAMPLING), anchor="w", font=self.gui_font)
        self.postprocessing_zoom_resampling_label.place(x=5, y=30, width=60, height=20)

        self.postprocessing_zoom_resampling_combobox = ttk.Combobox(self.postprocessing_labelframe, values=ZOOM_RESAMPLING_TYPES_NAMES, font=self.gui_font, state='readonly')
        self.postprocessing_zoom_resampling_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.postprocessing_zoom_resampling_combobox.place(x=70, y=30, width=90, height=20)
        self.postprocessing_zoom_resampling_combobox.set(DEFAULT_ZOOM_RESAMPLING_NAME)

        # vertical flip
        self.postprocessing_vertical_flip_variable = tk.StringVar(value="OFF")
        self.postprocessing_vertical_flip_checkbutton = tk.Checkbutton(self.postprocessing_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_VERTICAL_FLIP),
                                                                       variable=self.postprocessing_vertical_flip_variable, anchor="w",
                                                                       onvalue="ON", offvalue="OFF", font=self.gui_font,
                                                                       command=self.gui_reload_image_on_gui_element_change)
        self.postprocessing_vertical_flip_checkbutton.place(x=5, y=55, width=150, height=20)

        # horizontal flip
        self.postprocessing_horizontal_flip_variable = tk.StringVar(value="OFF")
        self.postprocessing_horizontal_flip_checkbutton = tk.Checkbutton(self.postprocessing_labelframe,
                                                                         text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_HORIZONTAL_FLIP),
                                                                         variable=self.postprocessing_horizontal_flip_variable, anchor="w",
                                                                         onvalue="ON", offvalue="OFF", font=self.gui_font,
                                                                         command=self.gui_reload_image_on_gui_element_change)
        self.postprocessing_horizontal_flip_checkbutton.place(x=5, y=75, width=170, height=20)

        # rotate
        self.postprocessing_rotate_label = tk.Label(self.postprocessing_labelframe, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_ROTATE), anchor="w",
                                                    font=self.gui_font)
        self.postprocessing_rotate_label.place(x=5, y=100, width=60, height=20)
        self.postprocessing_rotate_combobox = ttk.Combobox(self.postprocessing_labelframe,
                                                           values=ROTATE_TYPES_NAMES, font=self.gui_font, state='readonly')
        self.postprocessing_rotate_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.postprocessing_rotate_combobox.place(x=50, y=100, width=110, height=20)
        self.postprocessing_rotate_combobox.set(DEFAULT_ROTATE_NAME)

        ########################
        # IMAGE BOX            #
        ########################
        self.image_preview_labelframe = tk.LabelFrame(self.main_frame, text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_PREVIEW), font=self.gui_font)
        self.image_preview_labelframe.place(x=170, y=5, relwidth=1, relheight=1, height=-10, width=-375)

        self.image_preview_canvasframe = tk.Frame(self.image_preview_labelframe)
        self.image_preview_canvasframe.place(x=5, y=5, relwidth=1, relheight=1, height=-10, width=-10)






        ###############################################################################################################
        ############ menu
        ###############################################################################################################
        self.menubar = tk.Menu(master)

        # file submenu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_OPEN_FILE),
            command=lambda: self.open_image_file(),
            accelerator="Ctrl+O",
        )
        master.bind_all("<Control-o>", lambda x: self.open_image_file())

        self.filemenu.add_command(
            label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_SAVE_AS),
            command=lambda: self.export_image_file(),
            accelerator="Ctrl+S",
        )
        master.bind_all("<Control-s>", lambda x: self.export_image_file())
        self.filemenu.entryconfig(1, state="disabled")

        self.filemenu.add_command(
            label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_SAVE_RAW_DATA),
            command=lambda: self.export_raw_file(),
            accelerator="Ctrl+D",
        )
        master.bind_all("<Control-d>", lambda x: self.export_raw_file())
        self.filemenu.entryconfig(2, state="disabled")

        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_QUIT),
                                  command=lambda: self.quit_program(), accelerator="Ctrl+Q")
        master.bind_all("<Control-q>", lambda x: self.quit_program())
        self.menubar.add_cascade(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_FILE), menu=self.filemenu)

        # options submenu
        self.optionsmenu = tk.Menu(self.menubar, tearoff=0)

        self.languagemenu = tk.Menu(self.optionsmenu, tearoff=0)
        self.optionsmenu.add_cascade(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE), menu=self.languagemenu)

        self.languagemenu.add_radiobutton(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_EN), variable=self.current_program_language, value="EN", command=lambda: self.set_program_language())
        self.languagemenu.add_radiobutton(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_PL), variable=self.current_program_language, value="PL", command=lambda: self.set_program_language())

        self.backgroundmenu = tk.Menu(self.optionsmenu, tearoff=0)
        self.optionsmenu.add_cascade(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_COLOR), menu=self.backgroundmenu)
        self.backgroundmenu.add_radiobutton(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_GRAY), variable=self.current_background_color, value="#595959", command=lambda: self.reload_image_callback(None))
        self.backgroundmenu.add_radiobutton(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_BLACK), variable=self.current_background_color, value="#000000", command=lambda: self.reload_image_callback(None))
        self.backgroundmenu.add_radiobutton(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_WHITE), variable=self.current_background_color, value="#FFFFFF", command=lambda: self.reload_image_callback(None))

        self.menubar.add_cascade(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_OPTIONS), menu=self.optionsmenu)

        # help submenu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_HELPMENU_ABOUT), command=lambda: self.show_about_window(), accelerator="Ctrl+H")
        master.bind_all("<Control-h>", lambda x: self.show_about_window())
        self.menubar.add_cascade(label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_HELPMENU_HELP), menu=self.helpmenu)

        master.config(menu=self.menubar)

        ######################################################################################################
        #                           STARTUP LOGIC  (options menu logic)                                      #
        ######################################################################################################

        # set language on startup logic
        self.set_program_language()

    ######################################################################################################
    #                                             methods                                                #
    ######################################################################################################

    def get_translation_text(self, translation_str_id: str = "") -> str:
        for translation_entry in self.TRANSLATION_MEMORY:
            if translation_entry.id == translation_str_id:
                if translation_entry.text is not None:
                    return translation_entry.text
                else:
                    return translation_entry.default
        return "<missing_text>"

    def set_program_language(self) -> None:
        logger.info("Setting program's language to: " + self.current_program_language.get())

        json_path = os.path.join(self.MAIN_DIRECTORY, "data", "lang",
                                                      self.current_program_language.get() + ".json")
        try:
            new_translation_memory: List[TranslationEntry] = []
            translation_json_file = open(json_path, "rt", encoding="utf8")
            translations_dict: dict = json.loads(translation_json_file.read())['translation_strings']
            for translation_entry in self.TRANSLATION_MEMORY:
                json_translated_text: str = translations_dict.get(translation_entry.id)
                new_translation_memory.append(
                    TranslationEntry(id=translation_entry.id,
                                     default=translation_entry.default,
                                     text=json_translated_text
                                     )
                )
            self.TRANSLATION_MEMORY = new_translation_memory

        except Exception as error:
            logger.error(f"Couldn't load language strings from path: {json_path}. Error: {error}")
            return

        self.parameters_labelframe.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_PARAMETERS))
        self.width_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_WIDTH))
        self.height_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_HEIGHT))
        self.img_start_offset_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_START_OFFSET))
        self.img_end_offset_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_END_OFFSET))
        self.pixel_format_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PIXEL_FORMAT))
        self.endianess_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_ENDIANESS_TYPE))
        self.swizzling_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_SWIZZLING_TYPE))
        self.compression_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_COMPRESSION_TYPE))

        self.palette_parameters_labelframe.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PALETTE_PARAMETERS))
        self.palette_load_from_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_LOAD_FROM))
        self.palette_load_from_same_file_radio_button.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_SAME_FILE))
        self.palette_load_from_another_file_radio_button.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_ANOTHER_FILE))
        self.palette_palfile_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PALETTE_FILE))
        self.palette_palfile_button.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_BROWSE))
        self.palette_palformat_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PAL_FORMAT))
        self.palette_paloffset_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PAL_OFFSET))
        self.palette_endianess_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PALETTE_ENDIANESS))
        self.palette_ps2swizzle_checkbutton.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_PS2_PALETTE_SWIZZLE))

        self.image_preview_labelframe.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_IMAGE_PREVIEW))

        self.info_labelframe.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_LABELFRAME))
        self.infobox_file_name_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILENAME_LABEL), self.gui_params.img_file_name if self.opened_image else ""))
        self.infobox_file_size_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILE_SIZE), self.get_info_file_size_str() if self.opened_image else ""))
        self.infobox_pixel_x_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_X), str(self.pixel_x) if self.opened_image else ""))
        self.infobox_pixel_y_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_Y), str(self.pixel_y) if self.opened_image else ""))
        self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_OFFSET), str(self.pixel_offset) if self.opened_image else ""))
        self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_pixel_value_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE), self.pixel_value_str, self.pixel_value_rgba) if self.opened_image else self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE), ""))

        self.controls_labelframe.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_LABELFRAME))
        self.controls_all_info_label.set_html(self._get_html_for_controls_label())

        self.postprocessing_labelframe.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_LABELFRAME))
        self.postprocessing_zoom_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_ZOOM))
        self.postprocessing_zoom_resampling_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_RESAMPLING))
        self.postprocessing_vertical_flip_checkbutton.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_VERTICAL_FLIP))
        self.postprocessing_horizontal_flip_checkbutton.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_HORIZONTAL_FLIP))
        self.postprocessing_rotate_label.config(text=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POST_PROCESSING_ROTATE))

        self.filemenu.entryconfigure(0, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_OPEN_FILE))
        self.filemenu.entryconfigure(1, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_SAVE_AS))
        self.filemenu.entryconfigure(2, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_SAVE_RAW_DATA))
        self.filemenu.entryconfigure(4, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_QUIT))
        self.menubar.entryconfigure(1, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_FILEMENU_FILE))

        self.optionsmenu.entryconfigure(0, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE))
        self.optionsmenu.entryconfigure(1, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_COLOR))
        self.languagemenu.entryconfigure(0, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_EN))
        self.languagemenu.entryconfigure(1, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_LANGUAGE_PL))
        self.backgroundmenu.entryconfigure(0, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_GRAY))
        self.backgroundmenu.entryconfigure(1, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_BLACK))
        self.backgroundmenu.entryconfigure(2, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_BACKGROUND_WHITE))
        self.menubar.entryconfigure(2, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_OPTIONSMENU_OPTIONS))

        self.helpmenu.entryconfigure(0, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_HELPMENU_ABOUT))
        self.menubar.entryconfigure(3, label=self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_HELPMENU_HELP))

        # save current language to config file
        self.user_config.set("config", ConfigKeys.CURRENT_PROGRAM_LANGUAGE, self.current_program_language.get())
        with open(self.user_config_file_name, "w") as configfile:
            self.user_config.write(configfile)

    def reload_image_callback(self, event):
        self.gui_reload_image_on_gui_element_change()
        self.parameters_box_disable_enable_logic()
        self.master.focus()

        # save current canvas color to config file
        self.user_config.set("config", ConfigKeys.CURRENT_CANVAS_COLOR, self.current_background_color.get())
        with open(self.user_config_file_name, "w") as configfile:
            self.user_config.write(configfile)

    def check_if_paletted_format_chosen(self, pixel_format: str) -> bool:
        for format_name in PALETTE_FORMATS_REGEX_NAMES:
            if format_name in pixel_format:
                return True
        return False

    def parameters_box_disable_enable_logic(self):
        if self.check_if_paletted_format_chosen(self.pixel_format_combobox.get().lower()):
            for child in self.palette_parameters_labelframe.winfo_children():
                if child.widgetName == "ttk::combobox":
                    child.configure(state='readonly')
                else:
                    child.configure(state='normal')
            self.palette_parameters_labelframe.configure(fg='black')
        else:
            for child in self.palette_parameters_labelframe.winfo_children():
                child.configure(state='disable')
            self.palette_parameters_labelframe.configure(fg='grey')


    def quit_program(self) -> bool:
        logger.info("Quit GUI...")
        self.master.destroy()
        return True

    def _get_html_for_infobox_label(self, text_header: str, text_value: str) -> str:
        html: str = f'''<div style="font-family: Arial; font-size: 8px;">
                        <span>{text_header}</span>
                        <span style="color: blue">{text_value}</span>
                        </div>
        '''
        return html

    def _get_line_for_controls_html_str(self, action_text: str, shortcut_text: str) -> str:
        return f'''<span>{action_text} - </span> <span style="color: blue">{shortcut_text}</span><br>'''

    def _get_html_for_controls_label(self) -> str:
        html: str = f'''<div style="font-family: Arial; font-size: 8px; row-gap:24px;">
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_IMG_WIDTH), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_WIDTH))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_IMG_HEIGHT), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_IMG_HEIGHT))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_DOUBLE_HALVE_WIDTH), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_DOUBLE_HALVE_WIDTH))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_BYTE), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_BYTE))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_STEP_BY_ROW), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_STEP_BY_ROW))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_PIXEL_FORMAT), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_PIXEL_FORMAT))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_ENDIANESS), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_ENDIANESS))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_SWIZZLING), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_SWIZZLING))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_COMPRESSION), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_COMPRESSION))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_RELOAD_IMG), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_RELOAD_IMG))}
                        {self._get_line_for_controls_html_str(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_ACTION_ZOOM), self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_CONTROLS_SHORTCUT_ZOOM))}
                        </div>
        '''
        return html

    def _get_html_for_infobox_pixel_value_label(self, text_header: str, pixel_value_str: str, pixel_rgba_value: bytes) -> str:
        hex_result_str: str = ""

        for i in range(3):
            hex_byte_str: str = convert_bytes_to_hex_string(pixel_rgba_value[i:i + 1]).strip()
            hex_result_str += hex_byte_str

        html: str = f'''<div style="font-family: Arial; font-size: 8px;">
                        <span>{text_header}</span>
                        <span style="color: blue">{pixel_value_str}</span>
                        <span style="color:#{hex_result_str};"> ⬛</span>
                        </div>
        '''
        return html

    def validate_spinbox(self, new_value):
        return new_value.isdigit() or new_value == ""

    def get_spinbox_value(self, spinbox: tk.Spinbox) -> int:
        if spinbox.get() == "":
            return 0
        else:
            return int(spinbox.get())

    def checkbox_value_to_bool(self, checkbox_value: str) -> bool:
        if checkbox_value.upper() == "ON":
            return True
        return False

    def get_gui_params_from_gui_elements(self) -> bool:
        # image parameters
        self.gui_params.img_height = self.get_spinbox_value(self.height_spinbox)
        self.gui_params.img_width = self.get_spinbox_value(self.width_spinbox)
        self.gui_params.pixel_format = self.pixel_format_combobox.get()
        self.gui_params.endianess_type = self.endianess_combobox.get()
        self.gui_params.swizzling_type = self.swizzling_combobox.get()
        self.gui_params.compression_type = self.compression_combobox.get()
        self.gui_params.img_start_offset = self.get_spinbox_value(self.img_start_offset_spinbox)
        self.gui_params.img_end_offset = self.get_spinbox_value(self.img_end_offset_spinbox)

        # palette parameters
        self.gui_params.palette_loadfrom_value = self.palette_load_from_variable.get()
        self.gui_params.palette_format = self.palette_format_combobox.get()
        self.gui_params.palette_offset = self.get_spinbox_value(self.palette_paloffset_spinbox)
        self.gui_params.palette_endianess = self.palette_endianess_combobox.get()
        self.gui_params.palette_ps2_swizzle_flag = self.checkbox_value_to_bool(self.palette_ps2swizzle_variable.get())

        # post-processing
        self.gui_params.zoom_name = self.postprocessing_zoom_combobox.get()
        self.gui_params.zoom_resampling_name = self.postprocessing_zoom_resampling_combobox.get()
        self.gui_params.vertical_flip_flag = self.checkbox_value_to_bool(self.postprocessing_vertical_flip_variable.get())
        self.gui_params.horizontal_flip_flag = self.checkbox_value_to_bool(self.postprocessing_horizontal_flip_variable.get())
        self.gui_params.rotate_name = self.postprocessing_rotate_combobox.get()

        return True

    def _calculate_image_dimensions_at_file_open(self) -> tuple:
        number_of_pixels: int = self.gui_params.total_file_size // 4
        pixel_sqrt: int = int(math.floor(math.sqrt(number_of_pixels)))
        return pixel_sqrt, pixel_sqrt

    def _calculate_end_offset_at_file_open(self, file_size: int) -> int:
        MAX_END_OFFSET: int = 5242880  # 5 MB
        if file_size > MAX_END_OFFSET:
            return MAX_END_OFFSET
        return file_size

    def get_info_file_size_str(self) -> str:
        return str(self.gui_params.total_file_size) + " (" + convert_from_bytes_to_mb_string(self.gui_params.total_file_size) + ")"

    def set_gui_elements_at_file_open(self) -> bool:
        # image parameters
        if not self.opened_image:
            self.pixel_format_combobox.set(DEFAULT_PIXEL_FORMAT_NAME)
            img_width, img_height = self._calculate_image_dimensions_at_file_open()
            self.current_width.set(img_width)
            self.current_height.set(img_height)

        self.swizzling_combobox.set(DEFAULT_SWIZZLING_NAME)
        self.compression_combobox.set(DEFAULT_COMPRESSION_NAME)
        self.current_start_offset.set("0")
        self.current_end_offset.set(str(self._calculate_end_offset_at_file_open(self.gui_params.total_file_size)))
        self.img_end_offset_spinbox.config(to=self.gui_params.total_file_size)  # set max value for end offset

        # palette parameters
        self.palette_load_from_variable.set(1)
        self.palette_load_from_same_file_radio_button.select()
        self.palette_format_combobox.set(DEFAULT_PALETTE_FORMAT_NAME)
        self.palette_current_paloffset.set("0")
        self.palette_endianess_combobox.set(DEFAULT_ENDIANESS_NAME)
        self.palette_ps2swizzle_variable.set("OFF")
        self.palette_ps2swizzle_checkbutton.deselect()
        self.parameters_box_disable_enable_logic()

        # info labels
        self.infobox_file_name_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILENAME_LABEL), self.gui_params.img_file_name))
        self.infobox_file_name_tooltip.text = self.gui_params.img_file_name
        self.infobox_file_size_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_FILE_SIZE), self.get_info_file_size_str()))
        self.infobox_pixel_x_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_X), ""))
        self.infobox_pixel_y_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_Y), ""))
        self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_OFFSET), ""))
        self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE), ""))

        # post-processing
        self.postprocessing_zoom_combobox.set(DEFAULT_ZOOM_NAME)
        self.postprocessing_zoom_resampling_combobox.set(DEFAULT_ZOOM_RESAMPLING_NAME)
        self.postprocessing_vertical_flip_variable.set("OFF")
        self.postprocessing_vertical_flip_checkbutton.deselect()
        self.postprocessing_horizontal_flip_variable.set("OFF")
        self.postprocessing_horizontal_flip_checkbutton.deselect()
        self.postprocessing_rotate_combobox.set(DEFAULT_ROTATE_NAME)

        return True

    def gui_reload_image_on_gui_element_change(self) -> bool:
        self.get_gui_params_from_gui_elements()

        # heat image logic
        if self.opened_image:
            self.opened_image.gui_params = self.gui_params
            self.opened_image.image_reload()
            self.init_image_preview_logic()
        else:
            logger.info("Image is not opened yet...")
        return True

    # File > Open
    def open_image_file(self) -> bool:
        try:
            in_file = filedialog.askopenfile(mode="rb", initialdir=self.current_open_file_directory_path)
            if not in_file:
                return False
            try:
                selected_directory = os.path.dirname(in_file.name)
                self.current_open_file_directory_path = selected_directory  # set directory path from history
                self.user_config.set("config", ConfigKeys.OPEN_FILE_DIRECTORY_PATH, selected_directory)  # save directory path to config file
                with open(self.user_config_file_name, "w") as configfile:
                    self.user_config.write(configfile)
            except Exception:
                pass
            in_file_path = in_file.name
            in_file_name = in_file_path.split("/")[-1]
        except Exception as error:
            logger.error("Failed to open file! Error: %s", error)
            messagebox.showwarning("Warning", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_FAILED_TO_OPEN_FILE))
            return False

        logger.info(f"Loading file {in_file_name}...")

        # gui params logic
        self.gui_params.img_file_path = in_file_path
        self.gui_params.img_file_name = in_file_name
        self.gui_params.total_file_size = os.path.getsize(in_file_path)
        self.set_gui_elements_at_file_open()
        self.get_gui_params_from_gui_elements()

        # heat image logic
        self.opened_image = HeatImage(self.gui_params)
        self.opened_image.image_reload()
        self.init_image_preview_logic()

        # menu bar logic
        self.filemenu.entryconfig(1, state="normal")
        self.filemenu.entryconfig(2, state="normal")

        logger.info("Image has been opened successfully")
        return True

    def open_palette_file(self) -> bool:
        try:
            in_file = filedialog.askopenfile(mode="rb", initialdir=self.current_open_palette_directory_path)
            if not in_file:
                return False
            try:
                selected_directory = os.path.dirname(in_file.name)
                self.current_open_palette_directory_path = selected_directory  # set directory path from history
                self.user_config.set("config", ConfigKeys.OPEN_PALETTE_DIRECTORY_PATH, selected_directory)  # save directory path to config file
                with open(self.user_config_file_name, "w") as configfile:
                    self.user_config.write(configfile)
            except Exception:
                pass
            in_file_path = in_file.name
            in_file_name = in_file_path.split("/")[-1]
        except Exception as error:
            logger.error("Failed to open file! Error: %s", error)
            messagebox.showwarning("Warning", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_FAILED_TO_OPEN_FILE))
            return False

        # gui params logic
        self.gui_params.palette_file_path = in_file_path

        # browse button logic
        self.gui_params.img_palette_name = in_file_name
        button_label_text: str = in_file_name
        if len(button_label_text) > 11:
            button_label_text = "..." + button_label_text[len(button_label_text) - 11:]
        self.palette_palfile_button.configure(text=button_label_text, fg='blue')

        self.gui_reload_image_on_gui_element_change()
        return True

    # File > Save As
    def export_image_file(self) -> bool:
        if self.opened_image:
            out_file = None
            try:
                out_file = filedialog.asksaveasfile(
                    mode="wb",
                    defaultextension="" if platform.uname().system == "Linux" else ".dds",
                    initialfile="exported_image",
                    initialdir=self.current_save_as_directory_path,
                    filetypes=((self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_DDS), "*.dds"),
                               (self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_PNG), "*.png"),
                               (self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_BMP), "*.bmp")),
                )
                try:
                    selected_directory = os.path.dirname(out_file.name)
                    self.current_save_as_directory_path = selected_directory  # set directory path from history
                    self.user_config.set("config", ConfigKeys.SAVE_AS_DIRECTORY_PATH, selected_directory)  # save directory path to config file
                    with open(self.user_config_file_name, "w") as configfile:
                        self.user_config.write(configfile)
                except Exception:
                    pass

            except Exception as error:
                logger.error(f"Error: {error}")
                messagebox.showwarning("Warning", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_FAILED_TO_SAVE_FILE))
            if out_file is None:
                return False  # user closed file dialog on purpose

            # pack converted RGBA data
            file_extension: str = get_file_extension_uppercase(out_file.name)
            pillow_wrapper = PillowWrapper()
            out_data = pillow_wrapper.get_pil_image_file_data_for_export2(
                self.preview_final_pil_image, pillow_format=file_extension
            )
            if not out_data:
                logger.error("Empty data to export!")
                messagebox.showwarning("Warning", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_EMPTY_IMAGE_DATA))
                return False

            out_file.write(out_data)
            out_file.close()
            messagebox.showinfo("Info", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_FILE_SAVED_SUCCESSFULLY))
            logger.info(f"Image has been exported successfully to {out_file.name}")
        else:
            logger.info("Image is not opened yet...")

        return True

    # File > Save Raw Data
    def export_raw_file(self) -> bool:
        if self.opened_image:
            out_file = None
            try:
                out_file = filedialog.asksaveasfile(
                    mode="wb",
                    defaultextension=".bin",
                    initialfile="exported_raw_data",
                    initialdir=self.current_save_raw_data_directory_path,
                    filetypes=((self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_EXPORT_FILETYPES_BINARY), "*.bin"), ),
                )
                try:
                    selected_directory = os.path.dirname(out_file.name)
                    self.current_save_raw_data_directory_path = selected_directory  # set directory path from history
                    self.user_config.set("config", ConfigKeys.SAVE_RAW_DATA_DIRECTORY_PATH, selected_directory)  # save directory path to config file
                    with open(self.user_config_file_name, "w") as configfile:
                        self.user_config.write(configfile)
                except Exception:
                    pass
            except Exception as error:
                logger.error(f"Error: {error}")
                messagebox.showwarning("Warning", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_FAILED_TO_SAVE_FILE))
            if out_file is None:
                return False  # user closed file dialog on purpose

            out_data: bytes = self.opened_image.encoded_image_data

            out_file.write(out_data)
            out_file.close()
            messagebox.showinfo("Info", self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_POPUPS_RAW_DATA_SAVED_SUCCESSFULLY))
            logger.info(f"Raw data has been exported successfully to {out_file.name}")
        else:
            logger.info("Image is not opened yet...")

        return True

    def show_about_window(self):
        if not any(isinstance(x, tk.Toplevel) for x in self.master.winfo_children()):
            AboutWindow(self)

    @staticmethod
    def set_text_in_box(in_box, in_text):
        in_box.config(state="normal")
        in_box.delete("1.0", tk.END)
        in_box.insert(tk.END, in_text)
        in_box.config(state="disabled")

    @staticmethod
    def close_toplevel_window(wind):
        wind.destroy()

    def init_image_preview_logic(self) -> bool:
        if self.opened_image.is_preview_error:
            self.execute_error_preview_logic()
        else:
            self.execute_image_preview_logic()
        return True

    def execute_error_preview_logic(self) -> bool:
        pil_img = Image.open(self.preview_image_path)
        pil_img = pil_img.resize((500, 367))

        if self.preview_instance:
            self.preview_instance.destroy()  # destroy canvas to prevent memory leak

        self.preview_instance = tk.Canvas(
            self.image_preview_canvasframe,
            bg="#595959",
            width=pil_img.width,
            height=pil_img.height,
            highlightthickness=0
        )

        self.ph_img = ImageTk.PhotoImage(pil_img)

        self.preview_instance.create_image(
            int(pil_img.width),
            int(pil_img.height),
            anchor="se",
            image=self.ph_img,
        )
        self.preview_instance.place(x=0, y=0)

        return True

    def execute_image_preview_logic(self) -> bool:
        logger.info("Init image preview...")
        start_time = time.time()
        preview_img_width: int = int(self.gui_params.img_width)
        preview_img_height: int = int(self.gui_params.img_height)
        preview_data_size: int = preview_img_width * preview_img_height * 4
        preview_data: bytes = self.opened_image.decoded_image_data[:preview_data_size]
        pil_img = None

        try:
            pil_img: Image = Image.frombuffer(
                "RGBA",
                (preview_img_width, preview_img_height),
                preview_data,
                "raw",
                "RGBA",
                0,
                1,
            )

            # post-processing logic start
            # zoom
            self.preview_zoom_value: float = get_zoom_value(self.gui_params.zoom_name)
            preview_img_width = int(self.preview_zoom_value * preview_img_width)
            preview_img_height = int(self.preview_zoom_value * preview_img_height)
            pil_img = pil_img.resize((preview_img_width, preview_img_height), get_resampling_type(self.gui_params.zoom_resampling_name))

            # flipping
            if self.gui_params.vertical_flip_flag:
                pil_img = pil_img.transpose(Transpose.FLIP_TOP_BOTTOM)
            if self.gui_params.horizontal_flip_flag:
                pil_img = pil_img.transpose(Transpose.FLIP_LEFT_RIGHT)

            # rotating
            rotate_id = get_rotate_id(self.gui_params.rotate_name)
            if rotate_id == "none":
                pass
            elif rotate_id == "rotate_90_left":
                temp_width = preview_img_width
                preview_img_width = preview_img_height
                preview_img_height = temp_width
                pil_img = pil_img.transpose(Transpose.ROTATE_90)
            elif rotate_id == "rotate_90_right":
                temp_width = preview_img_width
                preview_img_width = preview_img_height
                preview_img_height = temp_width
                pil_img = pil_img.transpose(Transpose.ROTATE_270)
            elif rotate_id == "rotate_180":
                pil_img = pil_img.transpose(Transpose.ROTATE_180)
            else:
                logger.warning(f"Not supported rotate type selected! Rotate_id: {rotate_id}")

            self.ph_img = ImageTk.PhotoImage(pil_img)

            if self.preview_instance:
                self.preview_instance.destroy()  # destroy canvas to prevent memory leak

            self.preview_instance = tk.Canvas(
                self.image_preview_canvasframe,
                bg=self.current_background_color.get(),
                width=preview_img_width,
                height=preview_img_height,
                highlightthickness=0
            )

            self.preview_instance.create_image(
                preview_img_width,
                preview_img_height,
                anchor="se",
                image=self.ph_img,
            )
            self.preview_instance.place(x=0, y=0)

        except Exception as error:
            logger.error(f"Error occurred while generating preview... Error: {error}")

        def _mouse_motion(event):

            # getting params
            image_format: ImageFormats = ImageFormats[self.gui_params.pixel_format]
            compression_id: str = get_compression_id(self.gui_params.compression_type)
            m_rotate_id = get_rotate_id(self.gui_params.rotate_name)
            bpp: int = get_bpp_for_image_format(image_format)
            bytes_per_pixel: float = convert_bpp_to_bytes_per_pixel_float(bpp)

            # post-processing logic
            x = int(math.ceil((event.x + 1) / self.preview_zoom_value))
            y = int(math.ceil((event.y + 1) / self.preview_zoom_value))

            if self.gui_params.vertical_flip_flag:
                y = self.gui_params.img_height - y + 1
            if self.gui_params.horizontal_flip_flag:
                x = self.gui_params.img_width - x + 1

            if m_rotate_id == "none":
                pass
            elif m_rotate_id == "rotate_90_left":
                temp_x = x
                x = self.gui_params.img_width - y + 1
                y = temp_x
            elif m_rotate_id == "rotate_90_right":
                temp_x = x
                x = y
                y = self.gui_params.img_height - temp_x + 1
            elif m_rotate_id == "rotate_180":
                x = self.gui_params.img_width - x + 1
                y = self.gui_params.img_height - y + 1
            else:
                logger.warning(f"Not supported rotate type selected! Rotate_id: {m_rotate_id}")

            self.pixel_x = x
            self.pixel_y = y

            # pixel offset logic
            self.pixel_offset = int((self.pixel_y - 1) * self.gui_params.img_width * bytes_per_pixel + self.pixel_x * bytes_per_pixel - bytes_per_pixel)
            pixel_offset_rgba: int = int((self.pixel_y - 1) * self.gui_params.img_width * 4 + self.pixel_x * 4 - 4)

            if self.pixel_offset + bytes_per_pixel <= (self.gui_params.img_end_offset - self.gui_params.img_start_offset):

                self.infobox_pixel_x_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_X), str(self.pixel_x)))
                self.infobox_pixel_y_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_Y), str(self.pixel_y)))

                if not is_compressed_image_format(image_format) and compression_id == "none":
                    pixel_value: bytearray = self.opened_image.encoded_image_data[self.pixel_offset: self.pixel_offset + int(bytes_per_pixel)]
                    self.pixel_value_str = convert_bytes_to_hex_string(pixel_value)
                    self.pixel_value_rgba = self.opened_image.decoded_image_data[pixel_offset_rgba: pixel_offset_rgba + 4]
                    self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_OFFSET), str(self.pixel_offset)))
                    self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_pixel_value_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE), self.pixel_value_str, self.pixel_value_rgba))
                else:
                    self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_OFFSET), "n/a"))
                    self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_label(self.get_translation_text(TranslationKeys.TRANSLATION_TEXT_INFO_PIXEL_VALUE), "n/a"))

        # assign final preview values
        self.preview_final_pil_image = pil_img

        self.preview_instance.bind('<Motion>', _mouse_motion)
        execution_time = time.time() - start_time
        logger.info(f"Image preview for pixel_format={self.gui_params.pixel_format} finished successfully. Time: {round(execution_time, 2)} seconds.")
        return True

# fmt: on
