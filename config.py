import appdirs
import os

APP_DATA_DIR = appdirs.user_data_dir("FilTranslator", False)
SCREENSHOT_DIR = os.path.join(APP_DATA_DIR, "screenshot.png")