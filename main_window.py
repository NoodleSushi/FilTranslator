import config as cfg
from typing import Union
import tkinter as tk
import PIL
import PIL.Image
import pyscreenshot
import pytesseract
import crop_window


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(className="FilTranslator", *args, **kwargs)
        self.iconbitmap("icon.ico")
        self.geometry("400x200")
        self.configure(bg="black")
        self.attributes("-topmost", True)

        self.is_busy: bool = False
        self.is_ocr_captured: bool = False

        self.trans_stringvar: tk.StringVar = tk.StringVar(value="Default Value")
        self.trans_label: WrappingLabel = WrappingLabel(self, textvariable=self.trans_stringvar,
                                                        wraplength=400, justify="left", fg="#fff", bg="#000")
        self.trans_label.config(font=("Roboto", 16))
        self.trans_label.pack(expand=True, fill=tk.X)

        self.ocr_button: tk.Button = tk.Button(self, text="OCR",
                                                borderwidth=0, fg="#fff", bg="#000", command=self._on_ocr_button_ocr)
        self.ocr_button.config(font=("Roboto", 16))
        self.ocr_button.pack()
        self.ocr_text: str = ""

    def update_all(self) -> None:
        self.update_idletasks()
        self.update()

    def _on_ocr_button_ocr(self) -> None:
        if self.is_busy:
            return
        self.withdraw()
        screenshot: PIL.Image = pyscreenshot.grab()
        screenshot.save(cfg.SCREENSHOT_DIR)
        crop_coords: Union[tuple, None] = crop_window.get_crop_coords(cfg.SCREENSHOT_DIR)
        if type(crop_coords) is tuple:
            screenshot_cropped = screenshot.crop(crop_coords)
            self.ocr_text: str = pytesseract.image_to_string(screenshot_cropped, lang="tgl")[:-2]
            self.is_ocr_captured = True
        self.deiconify()

    def get_is_ocr_captured(self) -> bool:
        if self.is_ocr_captured:
            self.is_ocr_captured = False
            return True
        return False


class WrappingLabel(tk.Label):
    def __init__(self, master=None, *args, **kwargs) -> None:
        super(WrappingLabel, self).__init__(master, *args, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))
