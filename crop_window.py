from typing import Union, List
import tkinter as tk

X1, Y1, X2, Y2 = 0, 1, 2, 3


class CropWindow(tk.Tk):
    def __init__(self):
        super(CropWindow, self).__init__(className="Crop Window")
        self.attributes("-fullscreen", True)
        self.config(cursor="none")
        self.focus_force()
        self.crop_canvas: CropCanvas

    def get_crop_coords(self, img_dir: str) -> Union[tuple, None]:
        self.crop_canvas = CropCanvas(self, img_dir)
        self.crop_canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        while self.crop_canvas.is_active:
            self.update_idletasks()
            self.update()
        crop_coords: Union[tuple, None] = self.crop_canvas.get_crop_coords()
        self.destroy()
        
        return crop_coords


class CropCanvas(tk.Canvas):
    def __init__(self, master, img_dir: str, *args, **kwargs) -> None:
        super(CropCanvas, self).__init__(master, highlightthickness=0, *args, **kwargs)
        # set screenshot as background
        self.screenshot_img: tk.PhotoImage = tk.PhotoImage(master=self, file=img_dir)
        self.create_image(0, 0, image=self.screenshot_img, anchor=tk.NW)
        self.is_pressing: bool = False
        self.is_finished_cropping: bool = False
        self.is_active = True
        self.crop_coords: List[int] = [0, 0, 0, 0]
        # bind input behaviors
        self.bind("<Motion>", self._binded_motion)
        self.bind("<Button-1>", self._binded_pressed)
        self.bind("<ButtonRelease-1>", self._binded_released)
        self.master.bind("<Escape>", self._binded_close)
        # initialize graphics
        self.window_border_rect = self.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), 
                                                        fill="", dash=(4, 2), outline="white")
        self.crop_rect = self.create_rectangle(0, 0, 0, 0, fill="", dash=(4, 2), outline="red")
        self.h_line = self.create_line(0, 0, 0, 0, dash=(4, 2), fill="red")
        self.v_line = self.create_line(0, 0, 0, 0, dash=(4, 2), fill="red")

    def _binded_motion(self, event) -> None:
        self.coords(self.window_border_rect, 0, 0, self.winfo_width() - 1, self.winfo_height() - 1)
        self.coords(self.h_line, 0, event.y, self.winfo_width(), event.y)
        self.coords(self.v_line, event.x, 0, event.x, self.winfo_height())
        if self.is_pressing:
            self.crop_coords[X2] = event.x
            self.crop_coords[Y2] = event.y
            self.coords(self.crop_rect, *self.crop_coords)

    def _binded_pressed(self, event) -> None:
        self.is_pressing = True
        self.crop_coords[X1] = event.x
        self.crop_coords[Y1] = event.y

    def _binded_released(self, event) -> None:
        if self.is_pressing:
            self.is_pressing = False
            self.crop_coords[X2] = event.x
            self.crop_coords[Y2] = event.y
            self.is_finished_cropping = True
            self.is_active = False

    def _binded_close(self, _event) -> None:
        if self.is_pressing:
            self.is_pressing = False
            self.coords(self.crop_rect, *([0]*4))
        else:
            self.is_active = False

    def get_crop_coords(self) -> Union[tuple, None]:
        if self.is_finished_cropping:
            return tuple(self.crop_coords)
        else:
            return None
