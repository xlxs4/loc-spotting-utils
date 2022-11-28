import logging
from sys import exit

from PySide6.QtWidgets import QApplication

from GUI import GCodeUtilsGUI
from IOUtils import read_config
from paths import get_path

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )
    logging.info("Logger initialized.")

    relative_paths = True
    CONFIG = read_config(get_path("config", relative_paths))
    if not CONFIG:
        logging.error("Loading the configuration file failed.")
        exit(1)
    logging.info("Configuration file loaded successfully.")

    WINDOW_CONFIG = CONFIG.window

    app = QApplication([])

    logging.info("Starting main window.")
    window = GCodeUtilsGUI(CONFIG, relative_paths)
    window.resize(
        WINDOW_CONFIG["dimension"]["width"],
        WINDOW_CONFIG["dimension"]["height"]
    )
    window.show()
    logging.info("Window rendered successfully.")

    exit(app.exec())
