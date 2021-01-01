from googletrans import Translator
import pyperclip
from time import sleep
import tkinter as tk
import dictionary
import re
import pyscreenshot
from PIL import ImageTk, Image
import pytesseract
import json
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
tk_label = WrappingLabel(window, textvariable = tk_label_str, wraplength=400, justify = "left", fg = "#fff", bg="#000")
tk_label.config(font=("Roboto", 16))
tk_label.pack(expand = True, fill=tk.X)

is_free = True

# im = Image.open("textile.png")
# print(pytesseract.image_to_string(im, lang="tgl"))


def do_ocr():
    if not is_free:
        return
    screenshot = pyscreenshot.grab()
    screenshot.save("screenshot.png")
    window.withdraw()
    # sleep(2)

    new_window = tk.Tk()
    new_window.attributes("-fullscreen", True)
    canvas = tk.Canvas(new_window, highlightthickness=0)
    canvas.pack(expand=tk.YES,fill=tk.BOTH)
    img = tk.PhotoImage(master = canvas, file="screenshot.png")
    canvas.create_image(0,0,image=img,anchor=tk.NW)
    new_window.mainloop()

    


tk_button  = tk.Button(window, text="OCR", borderwidth = 0, fg = "#fff", bg="#000", command = do_ocr)
tk_button.config(font=("Roboto", 16))
tk_button.pack()

results =translator.translate('magandang umaga')
print(results.text)

text = ""

def update():
    window.update_idletasks()
    window.update()

while True:
    sleep(0)
    new_text = pyperclip.paste()
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
                lang = translator.detect(text).lang
                translation = ""
                if lang == "en":
                    translation = translator.translate(text, dest='tl')
                else:
                    translation = translator.translate(text)
                    pass
                text_translated = translation.text
            except:
                text_translated = "GOOGLE TRANSLATE SERVICE ERROR"
        if text_translated == "":
            text_translated = "NO RESULTS"

        pyperclip.copy(text_translated)
        text = text_translated
        tk_label_str.set(text_translated)
        is_free = True
    # window.lift()
    update()
