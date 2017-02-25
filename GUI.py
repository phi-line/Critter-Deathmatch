import math
import tkinter as tk

class GUI(tk.Canvas):
    '''
        When creating an instance of this class, pass tkinter.Tk() to it like this:
        gui = GUI(tkinter.Tk()
    '''
    def __init__(self,master, canvas_x, canvas_y, *args, **kwargs):
        self.win_x = canvas_x
        self.win_y = canvas_y

        tk.Canvas.__init__(self, master=master, width=self.win_x, height=self.win_y, borderwidth=0, highlightthickness=0, bg="#888888")
        self.pack()

    def debug_overlay(self,object):
        x1 = object.location[0]
        y1 = self.win_y - int(object.location[1])

        x2 = object.target[0]
        y2 = self.win_y - object.target[1]

        theta = ((object.heading % 360) * 2 * math.pi) / 360
        x3 = x1 + 50*math.cos(theta)
        y3 = y1 + 50*math.sin(theta)

        if (x2 != 0 and y2 != 0):
            self.create_line(x1,y1,x2,y2, width=2, fill=object.color)
        else:
            self.create_line(x1,y1,x2,y2, width=2, fill='#999999')

        if(object.heading != 0):
            self.create_line(x1, y1, x3, y3, width=3, fill='#111111')

    def create_circle(self, x, y, r, color, **kwargs):
        #self.create_rectangle(x-r*6,y-r*6,x+r*6,y+r*6, fill='#444444', outline='#000000',width=2, stipple='gray75')
        return self.create_oval(x - r, y - r, x + r, y + r, fill=color, **kwargs)

    def add_object_to_draw(self,object):
        x = int(object.location[0])
        y = self.win_y - int(object.location[1])
        r = object.size
        c = object.color
        #print('DRAW: ',x,'\t',y)
        self.debug_overlay(object)
        self.create_circle(x,y,r,c,outline='#000000',width=2)

    def draw(self):
        tk.Canvas.update_idletasks(self)
        tk.Canvas.update(self)

    def clear(self):
        tk.Canvas.delete(self,"all")