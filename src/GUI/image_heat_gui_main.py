"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import math
import os
import sys
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk
from reversebox.common.logger import get_logger

# default app settings
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 700

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
        self.icon_dir = self.MAIN_DIRECTORY + "\\data\\icon.ico"
        self.gui_font = ('Arial', 8)

        try:
            self.master.iconbitmap(self.icon_dir)
        except tk.TclError:
            logger.info("Can't load the icon file from %s", self.icon_dir)

        ########################
        # MAIN FRAME           #
        ########################
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        ########################
        # IMAGE PARAMETERS BOX #
        ########################
        self.parameters_labelframe = tk.LabelFrame(self.main_frame, text="Image Parameters", font=self.gui_font)
        self.parameters_labelframe.place(x=5, y=5, width=160, height=310)

        ###################################
        # IMAGE PARAMETERS - IMAGE WIDTH  #
        ###################################
        self.width_label = tk.Label(self.parameters_labelframe, text="Img Width", anchor="w", font=self.gui_font)
        self.width_label.place(x=5, y=5, width=60, height=20)

        self.width_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.width_spinbox.place(x=5, y=25, width=60, height=20)

        ######################################
        # IMAGE PARAMETERS - IMAGE HEIGHT    #
        ######################################
        self.height_label = tk.Label(self.parameters_labelframe, text="Img Height", anchor="w", font=self.gui_font)
        self.height_label.place(x=80, y=5, width=60, height=20)

        self.height_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.height_spinbox.place(x=80, y=25, width=60, height=20)


        ###########################################
        # IMAGE PARAMETERS - IMAGE START OFFSET   #
        ###########################################
        self.img_start_offset_label = tk.Label(self.parameters_labelframe, text="Start Offset", anchor="w", font=self.gui_font)
        self.img_start_offset_label.place(x=5, y=50, width=60, height=20)

        self.img_start_offset_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.img_start_offset_spinbox.place(x=5, y=70, width=60, height=20)

        ##########################################
        # IMAGE PARAMETERS - IMAGE END OFFSET    #
        ##########################################
        self.img_end_offset_label = tk.Label(self.parameters_labelframe, text="End Offset", anchor="w", font=self.gui_font)
        self.img_end_offset_label.place(x=80, y=50, width=60, height=20)

        self.img_end_offset_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.img_end_offset_spinbox.place(x=80, y=70, width=60, height=20)

        ####################################
        # IMAGE PARAMETERS - PIXEL FORMAT  #
        ####################################
        self.pixel_format_label = tk.Label(self.parameters_labelframe, text="Pixel Format", anchor="w", font=self.gui_font)
        self.pixel_format_label.place(x=5, y=95, width=60, height=20)

        self.PIXEL_FORMATS = ["RGB8888", "RGB565"]
        self.pixel_format_combobox = ttk.Combobox(self.parameters_labelframe,
                                                  values=self.PIXEL_FORMATS, font=self.gui_font, state='readonly')
        self.pixel_format_combobox.place(x=5, y=115, width=135, height=20)
        self.pixel_format_combobox.set(self.PIXEL_FORMATS[0])

        ####################################
        # IMAGE PARAMETERS - SWIZZLING     #
        ####################################
        self.swizzling_label = tk.Label(self.parameters_labelframe, text="Swizzling Type", anchor="w", font=self.gui_font)
        self.swizzling_label.place(x=5, y=140, width=100, height=20)

        self.SWIZZLING_TYPES = ["None", "PS1 Swizzle", "PS2 Swizzle", "PSP Swizzle"]
        self.swizzling_combobox = ttk.Combobox(self.parameters_labelframe,
                                               values=self.SWIZZLING_TYPES, font=self.gui_font, state='readonly')
        self.swizzling_combobox.place(x=5, y=160, width=135, height=20)
        self.swizzling_combobox.set(self.SWIZZLING_TYPES[0])

        #####################################
        # IMAGE PARAMETERS - CHECKBOXES     #
        #####################################

        self.vertical_flip_checkbox = tk.Checkbutton(self.parameters_labelframe, text="V Flip (top-down)", anchor="w")
        self.vertical_flip_checkbox.place(x=5, y=190, width=140, height=20)

        self.horizontal_flip_checkbox = tk.Checkbutton(self.parameters_labelframe, text="H Flip (left-right)", anchor="w")
        self.horizontal_flip_checkbox.place(x=5, y=210, width=140, height=20)

        self.invert_colors_checkbox = tk.Checkbutton(self.parameters_labelframe, text="Invert colors", anchor="w")
        self.invert_colors_checkbox.place(x=5, y=230, width=140, height=20)


        ####################################
        # IMAGE PARAMETERS - ZOOM          #
        ####################################
        self.zoom_label = tk.Label(self.parameters_labelframe, text="Zoom", anchor="w", font=self.gui_font)
        self.zoom_label.place(x=5, y=260, width=100, height=20)

        self.ZOOM_TYPES = ["1x", "2x", "3x", "4x", "5x", "10x"]
        self.zoom_combobox = ttk.Combobox(self.parameters_labelframe,
                                          values=self.ZOOM_TYPES, font=self.gui_font, state='readonly')
        self.zoom_combobox.place(x=40, y=260, width=50, height=20)
        self.zoom_combobox.set(self.ZOOM_TYPES[0])





        ##########################
        # PALETTE PARAMETERS BOX #
        ##########################
        self.palette_parameters_labelframe = tk.LabelFrame(self.main_frame, text="Palette Parameters", font=self.gui_font)
        self.palette_parameters_labelframe.place(x=5, y=320, width=160, height=170)

        ##########################################
        # PALETTE PARAMETERS BOX - PALETTE TYPE  #
        ##########################################
        self.palette_type_label = tk.Label(self.palette_parameters_labelframe, text="Palette type", anchor="w", font=self.gui_font)
        self.palette_type_label.place(x=5, y=5, width=100, height=20)

        self.PALETTE_TYPES = ["RGB", "Other"]
        self.palette_type_combobox = ttk.Combobox(self.palette_parameters_labelframe,
                                                  values=self.PALETTE_TYPES, font=self.gui_font, state='readonly')
        self.palette_type_combobox.place(x=5, y=25, width=140, height=20)
        self.palette_type_combobox.set(self.PALETTE_TYPES[0])

        ##########################################
        # PALETTE PARAMETERS BOX - OFFSET  #
        ##########################################
        self.palette_offset_label = tk.Label(self.palette_parameters_labelframe, text="Palette offset", anchor="w", font=self.gui_font)
        self.palette_offset_label.place(x=5, y=45, width=90, height=20)

        self.palette_offset_spinbox = tk.Spinbox(self.palette_parameters_labelframe, from_=0, to=sys.maxsize)
        self.palette_offset_spinbox.place(x=5, y=65, width=60, height=20)




        ##########################
        # INFO BOX #
        ##########################
        self.info_labelframe = tk.LabelFrame(self.main_frame, text="Info", font=self.gui_font)
        self.info_labelframe.place(x=-170, y=5, width=165, height=160, relx=1)

        self.file_name_label = tk.Label(self.info_labelframe, text="File name:", font=self.gui_font, anchor="w")
        self.file_name_label.place(x=5, y=5, width=145, height=20)

        self.file_size_label = tk.Label(self.info_labelframe, text="File size:", font=self.gui_font, anchor="w")
        self.file_size_label.place(x=5, y=25, width=145, height=20)

        self.file_offset_label = tk.Label(self.info_labelframe, text="File offset:", font=self.gui_font, anchor="w")
        self.file_offset_label.place(x=5, y=45, width=145, height=20)

        self.file_displayed_label = tk.Label(self.info_labelframe, text="Displayed:", font=self.gui_font, anchor="w")
        self.file_displayed_label.place(x=5, y=65, width=145, height=20)

        self.mouse_x_label = tk.Label(self.info_labelframe, text="Mouse X:", font=self.gui_font, anchor="w")
        self.mouse_x_label.place(x=5, y=85, width=145, height=20)

        self.mouse_x_label = tk.Label(self.info_labelframe, text="Mouse Y:", font=self.gui_font, anchor="w")
        self.mouse_x_label.place(x=5, y=105, width=145, height=20)








        ########################
        # IMAGE BOX            #
        ########################
        self.image_labelframe = tk.LabelFrame(self.main_frame, text="Image preview", font=self.gui_font)
        self.image_labelframe.place(x=170, y=5, relwidth=1, relheight=1, height=-15, width=-345)

        ##############################
        # IMAGE BOX - IMAGE CANVAS   #
        ##############################

        self.PREVIEW_HEIGHT = 200
        self.PREVIEW_WIDTH = 300

        im = Image.new('RGB', (self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT))
        # draw = ImageDraw.Draw(im)
        # for x in range(100):
        #     draw.point((x, 15), fill="red")
        # draw.ellipse((25, 25, 75, 75), fill=(255, 6, 6))
        for x in range(self.PREVIEW_WIDTH):
            for y in range(math.floor(self.PREVIEW_HEIGHT / 2)):
                im.putpixel((x, y), (44, 44, 44))

        self.canvas = tk.Canvas(self.image_labelframe)
        self.image = ImageTk.PhotoImage(im)
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.canvas.place(x=5, y=5, height=self.PREVIEW_HEIGHT, width=self.PREVIEW_WIDTH)






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

        self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="Options", command=lambda: None)
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(
            label="About...", command=lambda: self.show_about_window()
        )
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        master.config(menu=self.menubar)

    ######################################################################################################
    #                                             methods                                                #
    ######################################################################################################

    def quit_program(self):
        logger.info("Quit GUI...")
        self.master.destroy()

    def open_file(self):
        try:
            in_file = filedialog.askopenfile(
                mode="rb"
            )
            if not in_file:
                return
            in_file_path = in_file.name
            in_file_name = in_file_path.split("/")[-1]
        except Exception as error:
            logger.error("Failed to open file! Error: %s", error)
            messagebox.showwarning("Warning", "Failed to open file!")
            return

        logger.info("Loading file %s...", in_file_name)

    def show_about_window(self):
        pass

    @staticmethod
    def set_text_in_box(in_box, in_text):
        in_box.config(state="normal")
        in_box.delete("1.0", tk.END)
        in_box.insert(tk.END, in_text)
        in_box.config(state="disabled")

    @staticmethod
    def close_toplevel_window(wind):
        wind.destroy()

    @staticmethod
    def web_callback(url):
        webbrowser.open_new(url)

# fmt: on
