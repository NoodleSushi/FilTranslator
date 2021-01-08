import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(className="FilTranslator", *args, **kwargs)
        self.iconbitmap("icon.ico")
        self.geometry("400x200")
        self.configure(bg="black")
        self.attributes("-topmost", True)

        self.trans_stringvar: tk.StringVar = tk.StringVar(value="Default Value")
        self.trans_label: WrappingLabel = WrappingLabel(self, textvariable=self.trans_stringvar, font=("Roboto", 16),
                                                        wraplength=400, justify="left", fg="#fff", bg="#000")
        self.trans_label.pack(expand=True, fill=tk.X)

        self.ocr_button: tk.Button = tk.Button(self, text="OCR", font=("Roboto", 16),
                                               borderwidth=0, fg="#fff", bg="#000")
        self.ocr_button.pack()

        self.copy_button: tk.Button = tk.Button(self, text="COPY", font=("Roboto", 16),
                                                borderwidth=0, fg="#fff", bg="#000")
        self.copy_button.pack()

    def update_all(self) -> None:
        self.update_idletasks()
        self.update()

    def set_trans_text(self, text: str) -> None:
        self.trans_stringvar.set(text)
    
    def get_trans_text(self) -> str:
        return self.trans_stringvar.get()


class WrappingLabel(tk.Label):
    def __init__(self, master=None, *args, **kwargs) -> None:
        super(WrappingLabel, self).__init__(master, *args, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))
