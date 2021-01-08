import appdirs
import os

APP_DATA_DIR = appdirs.user_data_dir("FilTranslator", False)
SCREENSHOT_DIR = os.path.join(APP_DATA_DIR, "screenshot.png")
INSTALLERS_DIR = os.path.join(APP_DATA_DIR, "installers")
TESSERACT_INSTALLER_EXE = os.path.join(INSTALLERS_DIR, "tesseract-ocr-setup.exe")
TESSERACT_INSTALLER_URL = 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0.20190623.exe'
TESSERACT_PROGRAM_EXE = "Tesseract-OCR/tesseract.exe"  # 'C:/Program Files/Tesseract-OCR/tesseract.exe'
