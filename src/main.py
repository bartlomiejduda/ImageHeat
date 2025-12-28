"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# Program tested on Python 3.11.6

import os
import sys
from typing import Final

import center_tk_window
from reversebox.common.logger import get_logger

from src.GUI.gui_main import ImageHeatGUI
from src.GUI.gui_root import ImageHeatRoot

logger = get_logger("main")

if getattr(sys, "frozen", False):
    MAIN_DIRECTORY = os.path.dirname(sys.executable)
    NIGHTLY_STR: str = os.getenv("NIGHTLY_STR", default="")
    if len(NIGHTLY_STR) < 1:
        NIGHTLY_STR = "(NIGHTLY)" if "nightly" in os.path.abspath(sys.executable).lower() else ""
else:
    MAIN_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    NIGHTLY_STR: str = os.getenv("NIGHTLY_STR", default="")


VERSION_NUM: Final[str] = "v0.43.0"


def main():
    """
    Main function of this program.
    It will run ImageHeat in GUI mode.
    """

    logger.info("Starting main...")

    root: ImageHeatRoot = ImageHeatRoot(className="ImageHeat")
    ImageHeatGUI(root, VERSION_NUM + (" " + NIGHTLY_STR if len(NIGHTLY_STR) > 0 else ""), MAIN_DIRECTORY)  # start GUI
    root.lift()
    center_tk_window.center_on_screen(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

    logger.info("End of main...")


if __name__ == "__main__":
    main()
