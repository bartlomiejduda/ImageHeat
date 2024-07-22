"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import math
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from PIL import Image, ImageTk
from reversebox.common.logger import get_logger
from tkhtmlview import HTMLLabel

from src.GUI.about_window import AboutWindow
from src.GUI.gui_params import GuiParams
from src.Image.constants import PIXEL_FORMATS_NAMES, SWIZZLING_TYPES
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

        ######################################
        # IMAGE PARAMETERS - IMAGE HEIGHT    #
        ######################################
        self.height_label = tk.Label(self.parameters_labelframe, text="Img Height", anchor="w", font=self.gui_font)
        self.height_label.place(x=80, y=5, width=60, height=20)

        self.current_height = tk.StringVar()
        self.height_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_height, from_=0, to=sys.maxsize,
                                         command=self.gui_reload_image_on_gui_element_change)
        self.height_spinbox.place(x=80, y=25, width=60, height=20)


        ###########################################
        # IMAGE PARAMETERS - IMAGE START OFFSET   #
        ###########################################
        self.img_start_offset_label = tk.Label(self.parameters_labelframe, text="Start Offset", anchor="w", font=self.gui_font)
        self.img_start_offset_label.place(x=5, y=50, width=60, height=20)

        self.current_start_offset = tk.StringVar()
        self.img_start_offset_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_start_offset, from_=0, to=sys.maxsize,
                                                   command=self.gui_reload_image_on_gui_element_change)
        self.img_start_offset_spinbox.place(x=5, y=70, width=60, height=20)

        ##########################################
        # IMAGE PARAMETERS - IMAGE END OFFSET    #
        ##########################################
        self.img_end_offset_label = tk.Label(self.parameters_labelframe, text="End Offset", anchor="w", font=self.gui_font)
        self.img_end_offset_label.place(x=80, y=50, width=60, height=20)

        self.current_end_offset = tk.StringVar()
        self.img_end_offset_spinbox = tk.Spinbox(self.parameters_labelframe, textvariable=self.current_end_offset, from_=0, to=sys.maxsize,
                                                 command=self.gui_reload_image_on_gui_element_change)
        self.img_end_offset_spinbox.place(x=80, y=70, width=60, height=20)

        ####################################
        # IMAGE PARAMETERS - PIXEL FORMAT  #
        ####################################

        self.pixel_format_label = tk.Label(self.parameters_labelframe, text="Pixel Format", anchor="w", font=self.gui_font)
        self.pixel_format_label.place(x=5, y=95, width=60, height=20)

        def reload_image_callback(event):
            self.gui_reload_image_on_gui_element_change()

        self.pixel_format_combobox = ttk.Combobox(self.parameters_labelframe,
                                                  values=PIXEL_FORMATS_NAMES, font=self.gui_font, state='readonly')
        self.pixel_format_combobox.bind("<<ComboboxSelected>>", reload_image_callback)
        self.pixel_format_combobox.place(x=5, y=115, width=135, height=20)
        self.pixel_format_combobox.set(PIXEL_FORMATS_NAMES[0])

        ####################################
        # IMAGE PARAMETERS - SWIZZLING     #
        ####################################
        self.swizzling_label = tk.Label(self.parameters_labelframe, text="Swizzling Type", anchor="w", font=self.gui_font)
        self.swizzling_label.place(x=5, y=140, width=100, height=20)


        self.current_swizzling = tk.StringVar()
        self.swizzling_combobox = ttk.Combobox(self.parameters_labelframe,
                                               values=SWIZZLING_TYPES, textvariable=self.current_swizzling, font=self.gui_font, state='readonly')
        self.swizzling_combobox.place(x=5, y=160, width=135, height=20)
        self.swizzling_combobox.set(SWIZZLING_TYPES[0])



        ##########################
        # INFO BOX #
        ##########################

        self.info_labelframe = tk.LabelFrame(self.main_frame, text="Info", font=self.gui_font)
        self.info_labelframe.place(x=-200, y=5, width=195, height=110, relx=1)

        self.file_name_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("File name: ", ""), wrap=None)
        self.file_name_label.place(x=5, y=5, width=175, height=20)

        self.file_size_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("File size: ", ""), wrap=None)
        self.file_size_label.place(x=5, y=25, width=175, height=20)

        self.mouse_x_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Mouse X: ", ""), wrap=None)
        self.mouse_x_label.place(x=5, y=45, width=175, height=20)

        self.mouse_y_label = HTMLLabel(self.info_labelframe, html=self._get_html_for_infobox_label("Mouse Y: ", ""), wrap=None)
        self.mouse_y_label.place(x=5, y=65, width=175, height=20)


        ########################
        # IMAGE BOX            #
        ########################
        self.image_preview_labelframe = tk.LabelFrame(self.main_frame, text="Image preview", font=self.gui_font)
        self.image_preview_labelframe.place(x=170, y=5, relwidth=1, relheight=1, height=-15, width=-375)






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

    def get_gui_params_from_gui_elements(self) -> bool:
        self.gui_params.img_height = int(self.height_spinbox.get())
        self.gui_params.img_width = int(self.width_spinbox.get())
        self.gui_params.pixel_format = self.pixel_format_combobox.get()
        self.gui_params.img_start_offset = int(self.img_start_offset_spinbox.get())
        self.gui_params.img_end_offset = int(self.img_end_offset_spinbox.get())
        return True

    def calculate_image_dimensions(self) -> tuple:
        number_of_pixels: int = self.gui_params.total_file_size // 4
        pixel_sqrt: int = int(math.floor(math.sqrt(number_of_pixels)))
        return pixel_sqrt, pixel_sqrt

    def set_gui_elements_at_file_open(self) -> bool:
        self.pixel_format_combobox.set(PIXEL_FORMATS_NAMES[0])  # RGBA8888
        img_width, img_height = self.calculate_image_dimensions()
        self.current_width.set(img_width)
        self.current_height.set(img_height)
        self.current_start_offset.set("0")
        self.current_end_offset.set(str(self.gui_params.total_file_size))
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

        logger.info("Image has been opened successfully")
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

        try:
            pil_img = Image.frombuffer(
                "RGBA",
                (int(self.gui_params.img_width), int(self.gui_params.img_height)),
                self.opened_image.decoded_image_data,
                "raw",
                "RGBA",
                0,
                1,
            )

            self.ph_img = ImageTk.PhotoImage(pil_img)

            if self.preview_instance:
                self.preview_instance.destroy()  # destroy canvas to prevent memory leak

            self.preview_instance = tk.Canvas(
                self.image_preview_labelframe,
                bg="#595959",
                width=self.gui_params.img_width,
                height=self.gui_params.img_height,
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

        def mouse_motion(event):
            x, y = event.x, event.y
            self.mouse_x_label.set_html(self._get_html_for_infobox_label("Mouse X: ", str(x)))
            self.mouse_y_label.set_html(self._get_html_for_infobox_label("Mouse Y: ", str(y)))

        self.preview_instance.bind('<Motion>', mouse_motion)

        return True

# fmt: on
