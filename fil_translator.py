import os
import re
from typing import Tuple, Union

import tkinter as tk
import pyscreenshot
import PIL.Image
import pytesseract

import config as cfg
from crop_window import CropWindow
from main_window import MainWindow
from clipboard_watcher import ClipboardWatcher
from translator_thread import TranslatorThread


class FilTranslator:
    def __init__(self) -> None:
        if not os.path.exists(cfg.APP_DATA_DIR):
            os.mkdir(cfg.APP_DATA_DIR)
        pytesseract.pytesseract.tesseract_cmd = cfg.TESSERACT_PROGRAM_EXE
        self.clipboard_watcher: ClipboardWatcher = ClipboardWatcher()
        self.translator_thread: TranslatorThread = TranslatorThread()
        self.main_window: MainWindow = MainWindow()
        self.main_window.copy_button.config(command=self._on_copy_button_press)
        self.main_window.ocr_button.config(command=self._on_ocr_button_press)

    def update(self) -> bool:
        self.update_trans_text()
        if self.clipboard_watcher.is_changed():
            self.start_translator_thread(self.clipboard_watcher.get_new_text())
        
        try:
            self.main_window.update_all()
        except tk.TclError:
            return False
        
        return True
    
    def start_translator_thread(self, text: str) -> None:
        self.translator_thread = TranslatorThread()
        self.translator_thread.start_translating(text)
        self.main_window.set_trans_text("...")

    def update_trans_text(self) -> None:
        translator_results: Tuple[bool, str] = self.translator_thread.get_results()
        if translator_results[0]:
            self.main_window.set_trans_text(translator_results[1])
    
    def _on_copy_button_press(self) -> None:
        self.clipboard_watcher.copy(self.main_window.get_trans_text())

    def _on_ocr_button_press(self) -> None:
        self.main_window.withdraw()
        screenshot: PIL.Image = pyscreenshot.grab()
        screenshot.save(cfg.SCREENSHOT_DIR)
        crop_window: CropWindow = CropWindow()
        crop_coords: Union[tuple, None] = crop_window.get_crop_coords(cfg.SCREENSHOT_DIR)
        self.main_window.deiconify()
        if type(crop_coords) is tuple:
            screenshot_cropped = screenshot.crop(crop_coords)
            ocr_text: str = pytesseract.image_to_string(screenshot_cropped, lang="tgl")[:-2]
            ocr_text = re.sub('\n+', ' ', ocr_text)
            ocr_text = re.sub(' +', ' ', ocr_text)
            self.start_translator_thread(ocr_text)
