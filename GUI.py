import math
import tkinter as tk

class GUI(tk.Canvas):
    '''
        When creating an instance of this class, pass tkinter.Tk() to it like this:
        gui = GUI(tkinter.Tk()
    '''
    def __init__(self,master, world_x, world_y, *args, **kwargs):
        self.win_x = world_x
        self.win_y = world_y

        tk.Canvas.__init__(self, master=master, width=self.win_x, height=self.win_y, borderwidth=0, highlightthickness=0, bg="white")
        self.pack()

    def create_circle(self, x, y, r, color, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, fill=color, **kwargs)

    def add_object_to_draw(self,object):
        self.create_circle(object.location[0],object.location[1],object.size,object.color,outline='#000000',width=2)

    def draw(self):
        tk.Canvas.update_idletasks(self)
        tk.Canvas.update(self)

    def clear(self):
        tk.Canvas.delete(self,"all")