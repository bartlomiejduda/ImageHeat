"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import math
import os
import platform
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from PIL import Image, ImageTk
from PIL.Image import Transpose
from reversebox.common.common import (
    convert_bytes_to_hex_string,
    convert_from_bytes_to_mb_string,
    get_file_extension_uppercase,
)
from reversebox.common.logger import get_logger
from reversebox.image.common import (
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
    DEFAULT_PIXEL_FORMAT_NAME,
    DEFAULT_ROTATE_NAME,
    DEFAULT_SWIZZLING_NAME,
    DEFAULT_ZOOM_NAME,
    DEFAULT_ZOOM_RESAMPLING_NAME,
    ENDIANESS_TYPES_NAMES,
    PALETTE_FORMATS_NAMES,
    PIXEL_FORMATS_NAMES,
    ROTATE_TYPES_NAMES,
    SWIZZLING_TYPES_NAMES,
    ZOOM_RESAMPLING_TYPES_NAMES,
    ZOOM_TYPES_NAMES,
    get_compression_id,
    get_resampling_type,
    get_rotate_id,
    get_zoom_value,
)
from src.Image.heatimage import HeatImage

# default app settings
WINDOW_HEIGHT = 510
WINDOW_WIDTH = 1000

logger = get_logger(__name__)

# fmt: off


class ImageHeatGUI:
    def __init__(self, master: tk.Tk, in_version_num: str, in_main_directory: str):
        logger.info("GUI init...")
        self.master = master
        self.VERSION_NUM = in_version_num
        self.MAIN_DIRECTORY = in_main_directory
        master.title(f"ImageHeat {in_version_num}")
        master.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
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

        try:
            if platform.uname().system == "Linux":
                self.master.iconphoto(False, tk.PhotoImage(file=self.icon_path))
            else:
                self.master.iconbitmap(self.icon_path)
        except tk.TclError:
            logger.info("Can't load the icon file from %s", self.icon_path)

        ########################
        # MAIN FRAME           #
        ########################
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        ########################
        # IMAGE PARAMETERS BOX #
        ########################
        self.parameters_labelframe = tk.LabelFrame(self.main_frame, text="Image Parameters", font=self.gui_font)
        self.parameters_labelframe.place(x=5, y=5, width=160, height=300)

        ###################################
        # IMAGE PARAMETERS - IMAGE WIDTH  #
        ###################################
        self.width_label = tk.Label(self.parameters_labelframe, text="Img Width", anchor="w", font=self.gui_font)
        self.width_label.place(x=5, y=5, width=60, height=20)

        self.current_width = tk.StringVar(value="0")
        self.width_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_width, from_=0, to=sys.maxsize,
                                        command=self.gui_reload_image_on_gui_element_change)
        self.width_spinbox.place(x=5, y=25, width=60, height=20)
        self.width_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _decrease_width_by_arrow_key(event):
            self.width_spinbox.invoke("buttondown")
            self.master.focus()

        def _increase_width_by_arrow_key(event):
            self.width_spinbox.invoke("buttonup")
            self.master.focus()

        def _halve_width_by_shortcut(event):
            if int(self.current_width.get()) > 1:
                self.current_width.set(str(int(self.current_width.get()) // 2))
                self.reload_image_callback(event)
                self.master.focus()

        def _double_width_by_shortcut(event):
            self.current_width.set(str(int(self.current_width.get()) * 2))
            self.reload_image_callback(event)
            self.master.focus()

        self.master.bind("<Left>", _decrease_width_by_arrow_key)
        self.master.bind("<Right>", _increase_width_by_arrow_key)

        self.master.bind("<q>", _halve_width_by_shortcut)
        self.master.bind("<w>", _double_width_by_shortcut)

        ######################################
        # IMAGE PARAMETERS - IMAGE HEIGHT    #
        ######################################
        self.height_label = tk.Label(self.parameters_labelframe, text="Img Height", anchor="w", font=self.gui_font)
        self.height_label.place(x=80, y=5, width=60, height=20)

        self.current_height = tk.StringVar(value="0")
        self.height_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_height, from_=0, to=sys.maxsize,
                                         command=self.gui_reload_image_on_gui_element_change)
        self.height_spinbox.place(x=80, y=25, width=60, height=20)
        self.height_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _decrease_height_by_arrow_key(event):
            self.height_spinbox.invoke("buttondown")
            self.master.focus()

        def _increase_height_by_arrow_key(event):
            self.height_spinbox.invoke("buttonup")
            self.master.focus()

        self.master.bind("<Up>", _decrease_height_by_arrow_key)
        self.master.bind("<Down>", _increase_height_by_arrow_key)


        ###########################################
        # IMAGE PARAMETERS - IMAGE START OFFSET   #
        ###########################################
        self.img_start_offset_label = tk.Label(self.parameters_labelframe, text="Start Offset", anchor="w", font=self.gui_font)
        self.img_start_offset_label.place(x=5, y=50, width=60, height=20)

        self.current_start_offset = tk.StringVar(value="0")
        self.img_start_offset_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_start_offset, from_=0, to=sys.maxsize,
                                                   command=self.gui_reload_image_on_gui_element_change)
        self.img_start_offset_spinbox.place(x=5, y=70, width=60, height=20)
        self.img_start_offset_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _decrease_start_offset_by_arrow_key(event):
            self.img_start_offset_spinbox.invoke("buttondown")
            self.master.focus()

        def _increase_start_offset_by_arrow_key(event):
            self.img_start_offset_spinbox.invoke("buttonup")
            self.master.focus()

        self.master.bind("<Control-Down>", _decrease_start_offset_by_arrow_key)
        self.master.bind("<Control-Up>", _increase_start_offset_by_arrow_key)

        ##########################################
        # IMAGE PARAMETERS - IMAGE END OFFSET    #
        ##########################################
        self.img_end_offset_label = tk.Label(self.parameters_labelframe, text="End Offset", anchor="w", font=self.gui_font)
        self.img_end_offset_label.place(x=80, y=50, width=60, height=20)

        self.current_end_offset = tk.StringVar(value="0")
        self.img_end_offset_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_end_offset, from_=0, to=sys.maxsize,
                                                 command=self.gui_reload_image_on_gui_element_change)
        self.img_end_offset_spinbox.place(x=80, y=70, width=60, height=20)
        self.img_end_offset_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        def _decrease_end_offset_by_arrow_key(event):
            self.img_end_offset_spinbox.invoke("buttondown")
            self.master.focus()

        def _increase_end_offset_by_arrow_key(event):
            self.img_end_offset_spinbox.invoke("buttonup")
            self.master.focus()

        self.master.bind("<Shift-Down>", _decrease_end_offset_by_arrow_key)
        self.master.bind("<Shift-Up>", _increase_end_offset_by_arrow_key)

        ####################################
        # IMAGE PARAMETERS - PIXEL FORMAT  #
        ####################################

        self.pixel_format_label = tk.Label(self.parameters_labelframe, text="Pixel Format", anchor="w", font=self.gui_font)
        self.pixel_format_label.place(x=5, y=95, width=60, height=20)

        self.pixel_format_combobox = ttk.Combobox(self.parameters_labelframe,
                                                  values=PIXEL_FORMATS_NAMES, font=self.gui_font, state='readonly')
        self.pixel_format_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.pixel_format_combobox.place(x=5, y=115, width=135, height=20)
        self.pixel_format_combobox.set(DEFAULT_PIXEL_FORMAT_NAME)

        def _get_previous_pixel_format_by_key(event):
            selection = self.pixel_format_combobox.current()
            last = len(self.pixel_format_combobox['values']) - 1
            try:
                self.pixel_format_combobox.current(selection - 1)
            except tk.TclError:
                self.pixel_format_combobox.current(last)
            self.reload_image_callback(event)

        def _get_next_pixel_format_by_key(event):
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

        self.endianess_label = tk.Label(self.parameters_labelframe, text="Endianess Type", anchor="w", font=self.gui_font)
        self.endianess_label.place(x=5, y=140, width=100, height=20)

        self.current_endianess = tk.StringVar(value="none")
        self.endianess_combobox = ttk.Combobox(self.parameters_labelframe, values=ENDIANESS_TYPES_NAMES, textvariable=self.current_endianess,
                                               font=self.gui_font, state='readonly')
        self.endianess_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.endianess_combobox.place(x=5, y=160, width=135, height=20)
        self.endianess_combobox.set(DEFAULT_ENDIANESS_NAME)

        def _get_next_endianess_type_by_key(event):
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
        self.swizzling_label = tk.Label(self.parameters_labelframe, text="Swizzling Type", anchor="w", font=self.gui_font)
        self.swizzling_label.place(x=5, y=185, width=100, height=20)

        self.current_swizzling = tk.StringVar(value="none")
        self.swizzling_combobox = ttk.Combobox(self.parameters_labelframe,
                                               values=SWIZZLING_TYPES_NAMES, textvariable=self.current_swizzling, font=self.gui_font, state='readonly')
        self.swizzling_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.swizzling_combobox.place(x=5, y=205, width=135, height=20)
        self.swizzling_combobox.set(DEFAULT_SWIZZLING_NAME)

        def _get_previous_swizzling_type_by_key(event):
            selection = self.swizzling_combobox.current()
            last = len(self.swizzling_combobox['values']) - 1
            try:
                self.swizzling_combobox.current(selection - 1)
            except tk.TclError:
                self.swizzling_combobox.current(last)
            self.reload_image_callback(event)

        def _get_next_swizzling_type_by_key(event):
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
        self.compression_label = tk.Label(self.parameters_labelframe, text="Compression Type", anchor="w", font=self.gui_font)
        self.compression_label.place(x=5, y=230, width=100, height=20)

        self.current_compression = tk.StringVar(value="none")
        self.compression_combobox = ttk.Combobox(self.parameters_labelframe, values=COMPRESSION_TYPES_NAMES, textvariable=self.current_compression, font=self.gui_font, state='readonly')
        self.compression_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.compression_combobox.place(x=5, y=250, width=135, height=20)
        self.compression_combobox.set(DEFAULT_COMPRESSION_NAME)

        def _get_previous_compression_type_by_key(event):
            selection = self.compression_combobox.current()
            last = len(self.compression_combobox['values']) - 1
            try:
                self.compression_combobox.current(selection - 1)
            except tk.TclError:
                self.compression_combobox.current(last)
            self.reload_image_callback(event)

        def _get_next_compression_type_by_key(event):
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
        self.palette_parameters_labelframe = tk.LabelFrame(self.main_frame, text="Palette Parameters", font=self.gui_font)
        self.palette_parameters_labelframe.place(x=5, y=305, width=160, height=190)


        ########################################
        # PALETTE PARAMETERS BOX  - LOAD FROM  #
        ########################################
        self.palette_load_from_label = tk.Label(self.palette_parameters_labelframe, text="Load From", anchor="w", font=self.gui_font)
        self.palette_load_from_label.place(x=5, y=0, width=60, height=20)

        self.palette_load_from_variable = tk.IntVar(value=1)

        self.palette_load_from_same_file_radio_button = tk.Radiobutton(self.palette_parameters_labelframe,
                                                                       text="Same File", variable=self.palette_load_from_variable,
                                                                       value=1, command=self.gui_reload_image_on_gui_element_change,
                                                                       anchor="w", font=self.gui_font)
        self.palette_load_from_same_file_radio_button.place(x=65, y=0, width=90, height=20)
        self.palette_load_from_same_file_radio_button.select()

        self.palette_load_from_another_file_radio_button = tk.Radiobutton(self.palette_parameters_labelframe,
                                                                          text="Another File",
                                                                          variable=self.palette_load_from_variable,
                                                                          value=2, command=self.gui_reload_image_on_gui_element_change,
                                                                          anchor="w", font=self.gui_font)
        self.palette_load_from_another_file_radio_button.place(x=65, y=15, width=90, height=20)

        self.palette_palfile_label = tk.Label(self.palette_parameters_labelframe, text="Palette File", anchor="w",
                                              font=self.gui_font)
        self.palette_palfile_label.place(x=5, y=40, width=60, height=20)

        self.palette_palfile_button = tk.Button(self.palette_parameters_labelframe, text="Browse...",
                                                command=self.open_palette_file, font=self.gui_font)
        self.palette_palfile_button.place(x=70, y=40, width=80, height=20)

        ###########################################
        # PALETTE PARAMETERS BOX  - PAL OFFSET  #
        ###########################################

        self.palette_paloffset_label = tk.Label(self.palette_parameters_labelframe, text="Pal. Offset", anchor="w",
                                                font=self.gui_font)
        self.palette_paloffset_label.place(x=5, y=70, width=60, height=20)

        self.palette_current_paloffset = tk.StringVar(value="0")
        self.palette_paloffset_spinbox = tk.Spinbox(self.palette_parameters_labelframe, textvariable=self.palette_current_paloffset, from_=0, to=sys.maxsize,
                                                    command=self.gui_reload_image_on_gui_element_change)
        self.palette_paloffset_spinbox.place(x=75, y=70, width=70, height=20)
        self.palette_paloffset_spinbox.configure(validate="key", validatecommand=self.validate_spinbox_command)

        #################################################
        # PALETTE PARAMETERS BOX  - PALETTE ENDIANESS   #
        #################################################

        self.palette_endianess_label = tk.Label(self.palette_parameters_labelframe, text="Palette Endianess", anchor="w", font=self.gui_font)
        self.palette_endianess_label.place(x=5, y=95, width=100, height=20)

        self.palette_current_endianess = tk.StringVar(value="none")
        self.palette_endianess_combobox = ttk.Combobox(self.palette_parameters_labelframe, values=ENDIANESS_TYPES_NAMES, textvariable=self.palette_current_endianess,
                                                       font=self.gui_font, state='readonly')
        self.palette_endianess_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.palette_endianess_combobox.place(x=5, y=115, width=135, height=20)
        self.palette_endianess_combobox.set(DEFAULT_ENDIANESS_NAME)

        ###########################################
        # PALETTE PARAMETERS BOX  - PS2 SWIZZLE   #
        ###########################################

        self.palette_ps2swizzle_variable = tk.StringVar(value="OFF")
        self.palette_ps2swizzle_checkbutton = tk.Checkbutton(self.palette_parameters_labelframe,
                                                             text="PS2 Palette Swizzle",
                                                             variable=self.palette_ps2swizzle_variable,
                                                             anchor="w", onvalue="ON", offvalue="OFF",
                                                             font=self.gui_font, command=self.gui_reload_image_on_gui_element_change)
        self.palette_ps2swizzle_checkbutton.place(x=5, y=140, width=140, height=20)


        #####################################################
        # PALETTE PARAMETERS BOX  - INITIAL DISABLE LOGIC   #
        #####################################################

        self.parameters_box_disable_enable_logic()

        ##########################
        # FORCE RELOAD #
        ##########################

        def _force_reload_image_by_pressing_enter(event):
            self.reload_image_callback(event)

        self.master.bind("<Return>", _force_reload_image_by_pressing_enter)

        ##########################
        # INFO BOX #
        ##########################

        self.info_labelframe = tk.LabelFrame(self.main_frame, text="Info", font=self.gui_font)
        self.info_labelframe.place(x=-200, y=5, width=195, height=145, relx=1)

        self.file_name_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("File name: ", ""), wrap=None)
        self.file_name_label.place(x=5, y=5, width=185, height=18)

        self.file_size_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("File size: ", ""), wrap=None)
        self.file_size_label.place(x=5, y=25, width=175, height=18)

        self.infobox_pixel_x_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Pixel X: ", ""), wrap=None)
        self.infobox_pixel_x_label.place(x=5, y=45, width=175, height=18)

        self.infobox_pixel_y_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Pixel Y: ", ""), wrap=None)
        self.infobox_pixel_y_label.place(x=5, y=65, width=175, height=18)

        self.infobox_pixel_offset_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Pixel offset: ", ""), wrap=None)
        self.infobox_pixel_offset_label.place(x=5, y=85, width=175, height=18)

        self.infobox_pixel_value_hex_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Pixel value (hex): ", ""), wrap=None)
        self.infobox_pixel_value_hex_label.place(x=5, y=105, width=175, height=18)

        ##########################
        # CONTROLS BOX #
        ##########################

        self.controls_labelframe = tk.LabelFrame(self.main_frame, text="Controls", font=self.gui_font)
        self.controls_labelframe.place(x=-200, y=150, width=195, height=185, relx=1)

        self.controls_all_info_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_controls_label(), wrap=None)
        self.controls_all_info_label.place(x=5, y=5, width=185, height=160)

        ##########################
        # POST-PROCESSING BOX #
        ##########################

        self.postprocessing_labelframe = tk.LabelFrame(self.main_frame, text="Post-processing", font=self.gui_font)
        self.postprocessing_labelframe.place(x=-200, y=335, width=195, height=150, relx=1)

        # zoom
        self.postprocessing_zoom_label = tk.Label(self.postprocessing_labelframe, text="Zoom", anchor="w", font=self.gui_font)
        self.postprocessing_zoom_label.place(x=5, y=5, width=60, height=20)

        self.postprocessing_zoom_combobox = ttk.Combobox(self.postprocessing_labelframe, values=ZOOM_TYPES_NAMES, font=self.gui_font, state='readonly')
        self.postprocessing_zoom_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.postprocessing_zoom_combobox.place(x=45, y=5, width=70, height=20)
        self.postprocessing_zoom_combobox.set(DEFAULT_ZOOM_NAME)

        def _zoom_by_shortcut(event):
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
        self.postprocessing_zoom_resampling_label = tk.Label(self.postprocessing_labelframe, text="Resampling", anchor="w", font=self.gui_font)
        self.postprocessing_zoom_resampling_label.place(x=5, y=30, width=60, height=20)

        self.postprocessing_zoom_resampling_combobox = ttk.Combobox(self.postprocessing_labelframe, values=ZOOM_RESAMPLING_TYPES_NAMES, font=self.gui_font, state='readonly')
        self.postprocessing_zoom_resampling_combobox.bind("<<ComboboxSelected>>", self.reload_image_callback)
        self.postprocessing_zoom_resampling_combobox.place(x=70, y=30, width=90, height=20)
        self.postprocessing_zoom_resampling_combobox.set(DEFAULT_ZOOM_RESAMPLING_NAME)

        # vertical flip
        self.postprocessing_vertical_flip_variable = tk.StringVar(value="OFF")
        self.postprocessing_vertical_flip_checkbutton = tk.Checkbutton(self.postprocessing_labelframe, text="Vertical Flip (Top-Down)",
                                                                       variable=self.postprocessing_vertical_flip_variable, anchor="w",
                                                                       onvalue="ON", offvalue="OFF", font=self.gui_font,
                                                                       command=self.gui_reload_image_on_gui_element_change)
        self.postprocessing_vertical_flip_checkbutton.place(x=5, y=55, width=150, height=20)

        # horizontal flip
        self.postprocessing_horizontal_flip_variable = tk.StringVar(value="OFF")
        self.postprocessing_horizontal_flip_checkbutton = tk.Checkbutton(self.postprocessing_labelframe,
                                                                         text="Horizontal Flip (Left-Right)",
                                                                         variable=self.postprocessing_horizontal_flip_variable, anchor="w",
                                                                         onvalue="ON", offvalue="OFF", font=self.gui_font,
                                                                         command=self.gui_reload_image_on_gui_element_change)
        self.postprocessing_horizontal_flip_checkbutton.place(x=5, y=75, width=170, height=20)

        # rotate
        self.postprocessing_rotate_label = tk.Label(self.postprocessing_labelframe, text="Rotate", anchor="w",
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
        self.image_preview_labelframe = tk.LabelFrame(self.main_frame, text="Image preview", font=self.gui_font)
        self.image_preview_labelframe.place(x=170, y=5, relwidth=1, relheight=1, height=-10, width=-375)

        self.image_preview_canvasframe = tk.Frame(self.image_preview_labelframe)
        self.image_preview_canvasframe.place(x=5, y=5, relwidth=1, relheight=1, height=-10, width=-10)






        ###############################################################################################################
        ############ menu
        ###############################################################################################################
        self.menubar = tk.Menu(master)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Open File",
            command=lambda: self.open_image_file(),
            accelerator="Ctrl+O",
        )
        master.bind_all("<Control-o>", lambda x: self.open_image_file())

        self.export_label: str = "Save As..."
        self.filemenu.add_command(
            label=self.export_label,
            command=lambda: self.export_image_file(),
            accelerator="Ctrl+S",
        )
        master.bind_all("<Control-s>", lambda x: self.export_image_file())
        self.filemenu.entryconfig(self.export_label, state="disabled")

        self.export_raw_label: str = "Save Raw Data"
        self.filemenu.add_command(
            label=self.export_raw_label,
            command=lambda: self.export_raw_file(),
            accelerator="Ctrl+D",
        )
        master.bind_all("<Control-d>", lambda x: self.export_raw_file())
        self.filemenu.entryconfig(self.export_raw_label, state="disabled")

        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Quit", command=lambda: self.quit_program(), accelerator="Ctrl+Q"
        )
        master.bind_all("<Control-q>", lambda x: self.quit_program())
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(
            label="About...", command=lambda: self.show_about_window()
        )
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        master.config(menu=self.menubar)

    ######################################################################################################
    #                                             methods                                                #
    ######################################################################################################

    def reload_image_callback(self, event):
        self.gui_reload_image_on_gui_element_change()
        self.parameters_box_disable_enable_logic()
        self.master.focus()

    def check_if_paletted_format_chosen(self, pixel_format: str) -> bool:
        for format_name in PALETTE_FORMATS_NAMES:
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

    def _get_html_for_controls_label(self) -> str:
        html: str = '''<div style="font-family: Arial; font-size: 8px; row-gap:24px;">
                        <span>Img width - </span> <span style="color: blue">Left/Right</span><br>
                        <span>Img height - </span> <span style="color: blue">Up/Down</span><br>
                        <span>Double/halve width - </span> <span style="color: blue">Q/W</span><br>
                        <span>Start offset - </span> <span style="color: blue">CTRL+Up/CTRL+Down</span><br>
                        <span>End offset - </span> <span style="color: blue">SHIFT+Up/SHIFT+Down</span><br>
                        <span>Pixel format - </span> <span style="color: blue">Z/X</span><br>
                        <span>Endianess - </span> <span style="color: blue">E</span><br>
                        <span>Swizzling - </span> <span style="color: blue">K/L</span><br>
                        <span>Compression - </span> <span style="color: blue">O/P</span><br>
                        <span>Reload img - </span> <span style="color: blue">Enter</span><br>
                        <span>Zoom - </span> <span style="color: blue">Mouse Wheel</span><br>
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
        self.palette_current_paloffset.set("0")
        self.palette_endianess_combobox.set(DEFAULT_ENDIANESS_NAME)
        self.palette_ps2swizzle_variable.set("OFF")
        self.palette_ps2swizzle_checkbutton.deselect()
        self.parameters_box_disable_enable_logic()

        # info labels
        self.file_name_label.set_html(self._get_html_for_infobox_label("File name: ", self.gui_params.img_file_name))
        self.file_size_label.set_html(self._get_html_for_infobox_label("File size: ", str(self.gui_params.total_file_size) + " (" + convert_from_bytes_to_mb_string(self.gui_params.total_file_size) + ")"))
        self.infobox_pixel_x_label.set_html(self._get_html_for_infobox_label("Pixel X: ", ""))
        self.infobox_pixel_y_label.set_html(self._get_html_for_infobox_label("Pixel Y: ", ""))
        self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label("Pixel offset: ", ""))
        self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_label("Pixel value (hex): ", ""))

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

    def open_image_file(self) -> bool:
        try:
            in_file = filedialog.askopenfile(
                mode="rb"
            )
            if not in_file:
                return False
            in_file_path = in_file.name
            in_file_name = in_file_path.split("/")[-1]
        except Exception as error:
            logger.error("Failed to open file! Error: %s", error)
            messagebox.showwarning("Warning", "Failed to open file!")
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
        self.filemenu.entryconfig(self.export_label, state="normal")
        self.filemenu.entryconfig(self.export_raw_label, state="normal")

        logger.info("Image has been opened successfully")
        return True

    def open_palette_file(self) -> bool:
        try:
            in_file = filedialog.askopenfile(
                mode="rb"
            )
            if not in_file:
                return False
            in_file_path = in_file.name
        except Exception as error:
            logger.error("Failed to open file! Error: %s", error)
            messagebox.showwarning("Warning", "Failed to open file!")
            return False

        # gui params logic
        self.gui_params.palette_file_path = in_file_path

        # browse button logic
        self.palette_palfile_button.configure(text="File OK", fg='blue')

        self.gui_reload_image_on_gui_element_change()
        return True

    def export_image_file(self) -> bool:
        if self.opened_image:
            out_file = None
            try:
                out_file = filedialog.asksaveasfile(
                    mode="wb",
                    defaultextension="" if platform.uname().system == "Linux" else ".dds",
                    initialfile="exported_image",
                    filetypes=(("DDS files", "*.dds"), ("PNG files", "*.png"), ("BMP files", "*.bmp")),
                )
            except Exception as error:
                logger.error(f"Error: {error}")
                messagebox.showwarning("Warning", "Failed to save file!")
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
                messagebox.showwarning("Warning", "Empty image data! Export not possible!")
                return False

            out_file.write(out_data)
            out_file.close()
            messagebox.showinfo("Info", "File saved successfully!")
            logger.info(f"Image has been exported successfully to {out_file.name}")
        else:
            logger.info("Image is not opened yet...")

        return True

    def export_raw_file(self) -> bool:
        if self.opened_image:
            out_file = None
            try:
                out_file = filedialog.asksaveasfile(
                    mode="wb",
                    defaultextension=".bin",
                    initialfile="exported_raw_data",
                    filetypes=(("Binary files", "*.bin"), ),
                )
            except Exception as error:
                logger.error(f"Error: {error}")
                messagebox.showwarning("Warning", "Failed to save file!")
            if out_file is None:
                return False  # user closed file dialog on purpose

            out_data: bytes = self.opened_image.encoded_image_data

            out_file.write(out_data)
            out_file.close()
            messagebox.showinfo("Info", "Raw data saved successfully!")
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
                bg="#595959",
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

            # pixel offset logic
            pixel_offset: int = int((y - 1) * self.gui_params.img_width * bytes_per_pixel + x * bytes_per_pixel - bytes_per_pixel)
            pixel_offset_rgba: int = int((y - 1) * self.gui_params.img_width * 4 + x * 4 - 4)

            if pixel_offset + bytes_per_pixel <= (self.gui_params.img_end_offset - self.gui_params.img_start_offset):

                self.infobox_pixel_x_label.set_html(self._get_html_for_infobox_label("Pixel X: ", str(x)))
                self.infobox_pixel_y_label.set_html(self._get_html_for_infobox_label("Pixel Y: ", str(y)))

                if not is_compressed_image_format(image_format) and compression_id == "none":
                    pixel_value: bytearray = self.opened_image.encoded_image_data[pixel_offset: pixel_offset + int(bytes_per_pixel)]
                    pixel_value_str: str = convert_bytes_to_hex_string(pixel_value)
                    pixel_value_rgba: bytearray = self.opened_image.decoded_image_data[pixel_offset_rgba: pixel_offset_rgba + 4]
                    self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label("Pixel offset: ", str(pixel_offset)))
                    self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_pixel_value_label("Pixel value (hex): ", pixel_value_str, pixel_value_rgba))
                else:
                    self.infobox_pixel_offset_label.set_html(self._get_html_for_infobox_label("Pixel offset: ", "n/a"))
                    self.infobox_pixel_value_hex_label.set_html(self._get_html_for_infobox_label("Pixel value (hex): ", "n/a"))

        # assign final preview values
        self.preview_final_pil_image = pil_img

        self.preview_instance.bind('<Motion>', _mouse_motion)
        execution_time = time.time() - start_time
        logger.info(f"Image preview for pixel_format={self.gui_params.pixel_format} finished successfully. Time: {round(execution_time, 2)} seconds.")
        return True

# fmt: on
