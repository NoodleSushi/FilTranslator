import config as cfg
import main_window
import tkinter as tk
import googletrans
import pyperclip
import pytesseract
import os


class ClipBoardWatcher:
    def __init__(self) -> None:
        self.old_text = ""
        self.new_text = ""

    def is_changed(self) -> bool:
        pasted: str = pyperclip.paste()
        if pasted != self.new_text:
            self.old_text = self.new_text
            self.new_text = pasted
            return True
        return False


if __name__ == "__main__":
    if not os.path.exists(cfg.APP_DATA_DIR):
        os.mkdir(cfg.APP_DATA_DIR)
    pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
    translator = googletrans.Translator()
    main_window = main_window.MainWindow()
    clipboard_watcher = ClipBoardWatcher()
    while True:
        if clipboard_watcher.is_changed():
            pass
        try:
            main_window.update_all()
        except tk.TclError:
            break
