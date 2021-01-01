# COMPONENTS NEEDED:
# Google Translator
# Requests
# Clipboard
# GUI
# Screenshot
# Image Manipulation
# OCR (Tesseract)
# Json
import tkinter as tk
from googletrans import Translator
import pyperclip
from time import sleep
import dictionary
import re
import pyscreenshot
from PIL import ImageTk, Image
import pytesseract
import json
from cropper import get_crop
pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
translator = Translator()

window = tk.Tk(className = "Translator")
window.iconbitmap('icon.ico')
window.geometry("400x200")
window.configure(bg='black')
# window.overrideredirect(1)
window.attributes("-topmost", True)

class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

tk_label_str = tk.StringVar(value="Default Value")
# tk_transparency = tk.DoubleVar(value=0.5)
# window.attributes("-alpha", tk_transparency.get())
tk_label = WrappingLabel(window, textvariable = tk_label_str, wraplength=400, justify = "left", fg = "#fff", bg="#000")
tk_label.config(font=("Roboto", 16))
tk_label.pack(expand = True, fill=tk.X)

is_free = True

# im = Image.open("textile.png")
# print(pytesseract.image_to_string(im, lang="tgl"))





text = ""
new_text = ""

def copy_text(event):
    if not is_free:
        return
    global text
    text = tk_label_str.get()
    global new_text
    new_text = text
    pyperclip.copy(text)

window.bind("<Button-1>", copy_text)

def update():
    window.update_idletasks()
    window.update()


def do_ocr():
    if not is_free:
        return
    window.withdraw ()
    screenshot = pyscreenshot.grab()
    screenshot.save("screenshot.png")
    crop_coords = get_crop("screenshot.png")
    im = Image.open("screenshot.png").crop(crop_coords)
    im.save("cropped.png")
    im = Image.open("cropped.png")
    global new_text
    new_text = pytesseract.image_to_string(im, lang="tgl")[:-2]
    print("RESULTS: "+new_text)
    window.deiconify()
    # sleep(2)

tk_button  = tk.Button(window, text="OCR", borderwidth = 0, fg = "#fff", bg="#000", command = do_ocr)
tk_button.config(font=("Roboto", 16))
tk_button.pack()


while True:
    if new_text != text:
        is_free = False
        text = new_text
        tk_label_str.set("...")
        update()
        text_translated = ""
        
        #if it is just a word, use tagalog.com or else use google translate
        if re.match("^[A-Za-z0-9-]*$", new_text.strip()):
            #check if is in dictionary
            definitions: list = dictionary.translate(new_text)
            if len(definitions) > 0:
                definition = definitions[0]
                text_translated = definition["content"]+": \n\n"+definition["english"]
                # if len(definitions) > 0:
                # for definition in definitions:
                #     text_translated += definition["content"]+":\n- "+definition["english"]+"\n\n"
                # text_translated = text_translated.rstrip()
        if text_translated == "":
            try:
                print(text)
                lang = translator.detect(text).lang
                translation = ""
                if lang == "en":
                    print("it is english")
                    translation = translator.translate(text, dest='tl')
                else:
                    translation = translator.translate(text)
                # translation = translator.translate(text, dest='tl')
                text_translated = translation.text
                print("translated:"+ text_translated)
            except:
                text_translated = "GOOGLE TRANSLATE SERVICE ERROR"
        if text_translated == "":
            text_translated = "NO RESULTS"

        # pyperclip.copy(new_text)
        # text = text_translated
        text = new_text
        pyperclip.copy(new_text)
        tk_label_str.set(text_translated)
        is_free = True
    # window.lift()
    sleep(0)
    new_text = pyperclip.paste()
    update()
