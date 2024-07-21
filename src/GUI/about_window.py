import tkinter as tk
import webbrowser

import center_tk_window
from PIL import Image, ImageTk
from reversebox.common.logger import get_logger

logger = get_logger(__name__)


class AboutWindow:
    def __init__(self, gui_object):
        ABOUT_WINDOW_WIDTH = 400
        ABOUT_WINDOW_HEIGHT = 190
        self.about_window = tk.Toplevel(width=ABOUT_WINDOW_WIDTH, height=ABOUT_WINDOW_HEIGHT)
        self.about_window.wm_title("About ImageHeat")

        self.about_window.minsize(ABOUT_WINDOW_WIDTH, ABOUT_WINDOW_HEIGHT)
        self.about_window.maxsize(ABOUT_WINDOW_WIDTH, ABOUT_WINDOW_HEIGHT)
        self.about_window.resizable(False, False)
        self.about_window.wm_attributes("-toolwindow", "True")  # remove default tkinter icon
        self.about_window.attributes("-topmost", "true")  # about window always on top

        self.about_main_frame = tk.Frame(self.about_window, bg="#f0f0f0")
        self.about_main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.about_title_frame = tk.Frame(
            self.about_main_frame, bg="#f0f0f0", highlightbackground="#a6a6a6", highlightthickness=1
        )
        self.about_title_frame.place(x=5, y=5, width=390, height=70)

        self.about_description_frame = tk.Frame(
            self.about_main_frame, bg="#f0f0f0", highlightbackground="#a6a6a6", highlightthickness=1
        )
        self.about_description_frame.place(x=5, y=80, width=390, height=70)

        ICON_WIDTH = 60
        ICON_HEIGHT = 60
        self.canvas_for_icon = tk.Canvas(self.about_title_frame, bg="green", borderwidth=0, highlightthickness=0)
        self.canvas_for_icon.place(x=5, y=5, width=ICON_WIDTH, height=ICON_HEIGHT)
        try:
            ea_icon = Image.open(gui_object.icon_path)
            self.canvas_for_icon.image = ImageTk.PhotoImage(ea_icon.resize((ICON_WIDTH, ICON_HEIGHT)))
            self.canvas_for_icon.create_image(0, 0, image=self.canvas_for_icon.image, anchor="nw")
        except Exception as error:
            logger.error(f"Can't load the icon file from {gui_object.icon_path}. Error: {error}")

        self.about_title_label_tool_name_label = tk.Label(
            self.about_title_frame, text="ImageHeat", font=("Arial", 20), anchor="center"
        )
        self.about_title_label_tool_name_label.place(x=75, y=5, width=300, height=40)

        self.about_title_label_version_label = tk.Label(
            self.about_title_frame, text="Version: " + str(gui_object.VERSION_NUM), font=("Arial", 12), anchor="center"
        )
        self.about_title_label_version_label.place(x=75, y=45, width=300, height=20)

        copyright_text: str = (
            "Copyright 2024 © Bartlomiej Duda. All Rights Reserved.\n"
            "For the latest version visit ImageHeat Github page at\n"
        )
        self.about_description_copyright_label = tk.Label(
            self.about_description_frame, text=copyright_text, anchor="center"
        )
        self.about_description_copyright_label.place(x=5, y=0, width=380, height=60)

        github_link: str = "https://github.com/bartlomiejduda/ImageHeat"
        self.about_description_github_button = tk.Button(
            self.about_description_frame,
            text=github_link,
            command=lambda: self._open_browser_and_close_about_window(gui_object, github_link),
            anchor="center",
        )
        self.about_description_github_button.place(x=35, y=40, width=330, height=20)

        self.ok_button = tk.Button(self.about_main_frame, text="OK")
        self.ok_button.place(x=160, y=155, width=90, height=30)
        self.ok_button.bind(
            "<Button-1>",
            lambda event, arg=self.about_window: gui_object.close_toplevel_window(arg),
        )

        self.about_window.lift()
        self.about_window.focus_force()
        center_tk_window.center_on_screen(self.about_window)

    def _open_browser_and_close_about_window(self, gui_object, link_to_open):
        webbrowser.open(link_to_open)
        gui_object.close_toplevel_window(self.about_window)
