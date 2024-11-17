"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import math
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from PIL import Image, ImageTk
from reversebox.common.common import get_file_extension_uppercase
from reversebox.common.logger import get_logger
from reversebox.image.pillow_wrapper import PillowWrapper
from tkhtmlview import HTMLLabel

from src.GUI.about_window import AboutWindow
from src.GUI.gui_params import GuiParams
from src.Image.constants import (
    DEFAULT_PIXEL_FORMAT_NAME,
    PIXEL_FORMATS_NAMES,
    SWIZZLING_TYPES_NAMES,
)
from src.Image.heatimage import HeatImage

# default app settings
WINDOW_HEIGHT = 500
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
        self.icon_path = self.MAIN_DIRECTORY + "\\data\\img\\heat_icon.ico"
        self.gui_font = ('Arial', 8)
        self.opened_image: Optional[HeatImage] = None
        self.gui_params: GuiParams = GuiParams()
        self.preview_instance = None
        self.validate_spinbox_command = (master.register(self.validate_spinbox), '%P')

        try:
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
        self.parameters_labelframe.place(x=5, y=5, width=160, height=210)

        ###################################
        # IMAGE PARAMETERS - IMAGE WIDTH  #
        ###################################
        self.width_label = tk.Label(self.parameters_labelframe, text="Img Width", anchor="w", font=self.gui_font)
        self.width_label.place(x=5, y=5, width=60, height=20)

        self.current_width = tk.StringVar()
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

        self.master.bind("<Left>", _decrease_width_by_arrow_key)
        self.master.bind("<Right>", _increase_width_by_arrow_key)

        ######################################
        # IMAGE PARAMETERS - IMAGE HEIGHT    #
        ######################################
        self.height_label = tk.Label(self.parameters_labelframe, text="Img Height", anchor="w", font=self.gui_font)
        self.height_label.place(x=80, y=5, width=60, height=20)

        self.current_height = tk.StringVar()
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

        self.current_start_offset = tk.StringVar()
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

        self.current_end_offset = tk.StringVar()
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

        def reload_image_callback(event):
            self.gui_reload_image_on_gui_element_change()
            self.master.focus()

        self.pixel_format_combobox = ttk.Combobox(self.parameters_labelframe,
                                                  values=PIXEL_FORMATS_NAMES, font=self.gui_font, state='readonly')
        self.pixel_format_combobox.bind("<<ComboboxSelected>>", reload_image_callback)
        self.pixel_format_combobox.place(x=5, y=115, width=135, height=20)
        self.pixel_format_combobox.set(DEFAULT_PIXEL_FORMAT_NAME)

        def _get_previous_pixel_format_by_key(event):
            selection = self.pixel_format_combobox.current()
            last = len(self.pixel_format_combobox['values']) - 1
            try:
                self.pixel_format_combobox.current(selection - 1)
            except tk.TclError:
                self.pixel_format_combobox.current(last)
            reload_image_callback(event)

        def _get_next_pixel_format_by_key(event):
            selection = self.pixel_format_combobox.current()
            try:
                self.pixel_format_combobox.current(selection + 1)
            except tk.TclError:
                self.pixel_format_combobox.current(0)
            reload_image_callback(event)

        self.master.bind("<z>", _get_previous_pixel_format_by_key)
        self.master.bind("<x>", _get_next_pixel_format_by_key)

        ####################################
        # IMAGE PARAMETERS - SWIZZLING     #
        ####################################
        self.swizzling_label = tk.Label(self.parameters_labelframe, text="Swizzling Type", anchor="w", font=self.gui_font)
        self.swizzling_label.place(x=5, y=140, width=100, height=20)


        self.current_swizzling = tk.StringVar()
        self.swizzling_combobox = ttk.Combobox(self.parameters_labelframe,
                                               values=SWIZZLING_TYPES_NAMES, textvariable=self.current_swizzling, font=self.gui_font, state='readonly')
        self.swizzling_combobox.bind("<<ComboboxSelected>>", reload_image_callback)
        self.swizzling_combobox.place(x=5, y=160, width=135, height=20)
        self.swizzling_combobox.set(SWIZZLING_TYPES_NAMES[0])

        def _get_previous_swizzling_type_by_key(event):
            selection = self.swizzling_combobox.current()
            last = len(self.swizzling_combobox['values']) - 1
            try:
                self.swizzling_combobox.current(selection - 1)
            except tk.TclError:
                self.swizzling_combobox.current(last)
            reload_image_callback(event)

        def _get_next_swizzling_type_by_key(event):
            selection = self.swizzling_combobox.current()
            try:
                self.swizzling_combobox.current(selection + 1)
            except tk.TclError:
                self.swizzling_combobox.current(0)
            reload_image_callback(event)

        self.master.bind("<a>", _get_previous_swizzling_type_by_key)
        self.master.bind("<s>", _get_next_swizzling_type_by_key)

        ##########################
        # FORCE RELOAD #
        ##########################

        def _force_reload_image_by_pressing_enter(event):
            reload_image_callback(event)

        self.master.bind("<Return>", _force_reload_image_by_pressing_enter)

        ##########################
        # INFO BOX #
        ##########################

        self.info_labelframe = tk.LabelFrame(self.main_frame, text="Info", font=self.gui_font)
        self.info_labelframe.place(x=-200, y=5, width=195, height=110, relx=1)

        self.file_name_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("File name: ", ""), wrap=None)
        self.file_name_label.place(x=5, y=5, width=175, height=18)

        self.file_size_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("File size: ", ""), wrap=None)
        self.file_size_label.place(x=5, y=25, width=175, height=18)

        self.mouse_x_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Mouse X: ", ""), wrap=None)
        self.mouse_x_label.place(x=5, y=45, width=175, height=18)

        self.mouse_y_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Mouse Y: ", ""), wrap=None)
        self.mouse_y_label.place(x=5, y=65, width=175, height=18)

        ##########################
        # CONTROLS BOX #
        ##########################

        self.controls_labelframe = tk.LabelFrame(self.main_frame, text="Controls", font=self.gui_font)
        self.controls_labelframe.place(x=-200, y=115, width=195, height=170, relx=1)

        self.controls_img_width_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("Img width -  ", "Left/Right"), wrap=None)
        self.controls_img_width_label.place(x=5, y=5, width=175, height=18)

        self.controls_img_height_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("Img height -  ", "Up/Down"), wrap=None)
        self.controls_img_height_label.place(x=5, y=25, width=175, height=18)

        self.controls_start_offset_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("Start offset -  ", "CTRL+Up/CTRL+Down"), wrap=None)
        self.controls_start_offset_label.place(x=5, y=45, width=185, height=18)

        self.controls_end_offset_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("End offset -  ", "SHIFT+Up/SHIFT+Down"), wrap=None)
        self.controls_end_offset_label.place(x=5, y=65, width=185, height=18)

        self.controls_pixel_format_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("Pixel Format -  ", "Z/X"), wrap=None)
        self.controls_pixel_format_label.place(x=5, y=85, width=175, height=18)

        self.controls_swizzling_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("Swizzling -  ", "A/S"), wrap=None)
        self.controls_swizzling_label.place(x=5, y=105, width=175, height=18)

        self.controls_swizzling_label = HTMLLabel(self.controls_labelframe, html=self._get_html_for_infobox_label("Reload img -  ", "Enter"), wrap=None)
        self.controls_swizzling_label.place(x=5, y=125, width=175, height=18)


        ########################
        # IMAGE BOX            #
        ########################
        self.image_preview_labelframe = tk.LabelFrame(self.main_frame, text="Image preview", font=self.gui_font)
        self.image_preview_labelframe.place(x=170, y=5, relwidth=1, relheight=1, height=-15, width=-375)

        self.image_preview_canvasframe = tk.Frame(self.image_preview_labelframe)
        self.image_preview_canvasframe.place(x=5, y=5, relwidth=1, relheight=1, height=-10, width=-10)






        ###############################################################################################################
        ############ menu
        ###############################################################################################################
        self.menubar = tk.Menu(master)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Open File",
            command=lambda: self.open_file(),
            accelerator="Ctrl+O",
        )
        master.bind_all("<Control-o>", lambda x: self.open_file())

        self.export_label: str = "Save As..."
        self.filemenu.add_command(
            label=self.export_label, command=lambda: self.export_image_file()
        )
        self.filemenu.entryconfig(self.export_label, state="disabled")

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

    def validate_spinbox(self, new_value):
        return new_value.isdigit() or new_value == ""

    def get_spinbox_value(self, spinbox: tk.Spinbox) -> int:
        if spinbox.get() == "":
            return 0
        else:
            return int(spinbox.get())

    def get_gui_params_from_gui_elements(self) -> bool:
        self.gui_params.img_height = self.get_spinbox_value(self.height_spinbox)
        self.gui_params.img_width = self.get_spinbox_value(self.width_spinbox)
        self.gui_params.pixel_format = self.pixel_format_combobox.get()
        self.gui_params.swizzling_type = self.swizzling_combobox.get()
        self.gui_params.img_start_offset = self.get_spinbox_value(self.img_start_offset_spinbox)
        self.gui_params.img_end_offset = self.get_spinbox_value(self.img_end_offset_spinbox)
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
        self.pixel_format_combobox.set(DEFAULT_PIXEL_FORMAT_NAME)
        img_width, img_height = self._calculate_image_dimensions_at_file_open()
        self.current_width.set(img_width)
        self.current_height.set(img_height)
        self.current_start_offset.set("0")
        self.current_end_offset.set(str(self._calculate_end_offset_at_file_open(self.gui_params.total_file_size)))
        self.img_end_offset_spinbox.config(to=self.gui_params.total_file_size)  # set max value for end offset

        # info labels
        self.file_name_label.set_html(self._get_html_for_infobox_label("File name: ", self.gui_params.img_file_name))
        self.file_size_label.set_html(self._get_html_for_infobox_label("File size: ", str(self.gui_params.total_file_size)))
        self.mouse_x_label.set_html(self._get_html_for_infobox_label("Mouse X: ", str(0)))
        self.mouse_y_label.set_html(self._get_html_for_infobox_label("Mouse Y: ", str(0)))

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

    def open_file(self) -> bool:
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

        logger.info("Image has been opened successfully")
        return True

    def export_image_file(self) -> bool:
        if self.opened_image:
            out_file = None
            try:
                out_file = filedialog.asksaveasfile(
                    mode="wb",
                    defaultextension=".dds",
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
            out_data = pillow_wrapper.get_pil_image_file_data_for_export(
                self.opened_image.decoded_image_data, self.gui_params.img_width, self.gui_params.img_height, pillow_format=file_extension
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
        pil_img = Image.open(self.MAIN_DIRECTORY + "\\data\\img\\preview_not_supported.png")
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
        preview_data_size: int = int(self.gui_params.img_width) * int(self.gui_params.img_height) * 4
        preview_data: bytes = self.opened_image.decoded_image_data[:preview_data_size]
        try:
            pil_img = Image.frombuffer(
                "RGBA",
                (int(self.gui_params.img_width), int(self.gui_params.img_height)),
                preview_data,
                "raw",
                "RGBA",
                0,
                1,
            )

            self.ph_img = ImageTk.PhotoImage(pil_img)

            if self.preview_instance:
                self.preview_instance.destroy()  # destroy canvas to prevent memory leak

            self.preview_instance = tk.Canvas(
                self.image_preview_canvasframe,
                bg="#595959",
                width=self.gui_params.img_width,
                height=self.gui_params.img_height,
                highlightthickness=0
            )

            self.preview_instance.create_image(
                int(self.gui_params.img_width),
                int(self.gui_params.img_height),
                anchor="se",
                image=self.ph_img,
            )
            self.preview_instance.place(x=0, y=0)

        except Exception as error:
            logger.error(f"Error occurred while generating preview... Error: {error}")

        def _mouse_motion(event):
            x, y = event.x, event.y
            self.mouse_x_label.set_html(self._get_html_for_infobox_label("Mouse X: ", str(x)))
            self.mouse_y_label.set_html(self._get_html_for_infobox_label("Mouse Y: ", str(y)))

        self.preview_instance.bind('<Motion>', _mouse_motion)

        execution_time = time.time() - start_time
        logger.info(f"Image preview for pixel_format={self.gui_params.pixel_format} finished successfully. Time: {round(execution_time, 2)} seconds.")
        return True

# fmt: on
