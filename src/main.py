"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# Program tested on Python 3.11.6

import os
from typing import Final

import center_tk_window
from reversebox.common.logger import get_logger

from src.GUI.gui_main import ImageHeatGUI
from src.GUI.gui_root import ImageHeatRoot

VERSION_NUM: Final[str] = "v0.30.0"

logger = get_logger("main")

MAIN_DIRECTORY = os.getcwd()


def main():
    """
    Main function of this program.
    It will run ImageHeat in GUI mode.
    """

    logger.info("Starting main...")

    root: ImageHeatRoot = ImageHeatRoot(className="ImageHeat")
    ImageHeatGUI(root, VERSION_NUM, MAIN_DIRECTORY)  # start GUI
    root.lift()
    center_tk_window.center_on_screen(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

    logger.info("End of main...")


if __name__ == "__main__":
    main()
