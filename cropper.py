import tkinter as tk
out = (0,0,0,0)
is_done = False

def get_crop(img_dir: str):
    global out
    out = (0,0,0,0)
    global is_done
    is_done = False
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    class Thing(tk.Canvas):
        def __init__(self,master,*args,**kwargs):
            super().__init__(master, highlightthickness=0)
            self.x1 = 0
            self.y1 = 0
            self.x2 = 0
            self.y2 = 0
            self.is_pressing = False
            self.screenshot_img = tk.PhotoImage(master = self, file=img_dir)
            self.create_image(0,0,image=self.screenshot_img,anchor=tk.NW)
            self.rect_outline = self.create_rectangle(0,0,self.winfo_width(),self.winfo_height(), fill="", dash=(4, 2), outline="white")
            self.rect = self.create_rectangle(0,0,0,0, fill="", dash=(4, 2), outline="red")
            self.hline = self.create_line(0,0,0,0, dash=(4, 2), fill = "red")
            self.vline = self.create_line(0,0,0,0, dash=(4, 2), fill = "red")
            self.bind("<Motion>", self.motion)
            self.bind("<Button-1>", self.pressed)
            self.bind("<ButtonRelease-1>", self.released)
            master.bind("<Escape>", self.close)
        
        def motion(self, event):
            self.coords(self.rect_outline, 0, 0, self.winfo_width()-1, self.winfo_height()-1)
            self.coords(self.hline, 0, event.y, self.winfo_width(), event.y)
            self.coords(self.vline, event.x, 0, event.x, self.winfo_height())
            if self.is_pressing:
                self.x2 = event.x
                self.y2 = event.y
                self.coords(self.rect, self.x1, self.y1, self.x2, self.y2)
        
        def pressed(self, event):
            self.is_pressing = True
            self.x1 = event.x
            self.y1 = event.y
            pass
        
        def released(self, event):
            self.is_pressing = False
            self.x2 = event.x
            self.y2 = event.y
            global out
            out = (self.x1, self.y1, self.x2, self.y2)
            global is_done
            is_done = True
        
        def close(self, event):
            print("I CLOSE NOW")
            global is_done
            is_done = True

    canvas = Thing(master = root)
    canvas.pack(expand=tk.YES,fill=tk.BOTH)
    while not is_done:
        root.update_idletasks()
        root.update()
    root.destroy()
    return out