import math
import tkinter as tk

class GUI(tk.Canvas):
    '''
        When creating an instance of this class, pass tkinter.Tk() to it like this:
        gui = GUI(tkinter.Tk()
    '''
    def __init__(self, master, WINDOW_X_SIZE, WINDOW_Y_SIZE, *args, **kwargs):
        self.win_x_size = WINDOW_X_SIZE
        self.win_y_size = WINDOW_Y_SIZE

        self.resolution = 1

        self.display_x_min = 0
        self.display_y_min = 0
        self.display_x_max = 0
        self.display_y_max = 0

        self.pixel_x_min = 0
        self.pixel_y_min = 0
        self.pixel_x_max = self.win_x_size
        self.pixel_y_max = self.win_y_size

        tk.Canvas.__init__(self, master=master, width=WINDOW_X_SIZE, height=WINDOW_Y_SIZE, borderwidth=0, highlightthickness=0, bg="#888888")
        self.pack()

    def map_x_coordinate(self, worldX):
        xMin = self.display_x_min
        xMax = self.display_x_max
        if(worldX < self.display_x_min):
            x = -1
        elif(worldX > self.display_x_max):
            x = self.display_x_max + 1
        else:
            x = ((worldX - xMin) / (xMax - xMin)) * self.pixel_x_max
        return int(x)

    def map_y_coordinate(self, worldY):
        yMin = self.display_y_min
        yMax = self.display_y_max
        if (worldY < self.display_y_min):
            y = -1
        elif (worldY > self.display_y_max):
            y = self.display_y_max + 1
        else:
            y = ((worldY - yMin) / (yMax - yMin)) * self.pixel_y_max
        return int(y)

    def place_window(self, display_x_min, display_y_min, display_x_max, display_y_max,):
        self.resolution = 0

        self.display_x_min = display_x_min
        self.display_y_min = display_y_min
        self.display_x_max = display_x_max
        self.display_y_max = display_y_max

    def debug_overlay(self,object):
        x1 = self.map_x_coordinate(object.location[0])
        y1 = self.pixel_y_max - self.map_y_coordinate(object.location[1])

        x2 = self.map_x_coordinate(object.target[0])
        y2 = self.pixel_y_max - self.map_y_coordinate(object.target[1])

        theta = ((object.heading % 360) * 2 * math.pi) / 360
        x3 = int(x1 + 1.5*object.size*math.cos(theta))
        y3 = int(y1 + 1.5*object.size*math.sin(theta))

        if (object.drawNearestLines):
            xT = 0
            yT = 0
            for i in range(0, len(object.nearest)):
                color = '#%02x%02x%02x' % (int(i * 80), int(i * 80), int(i * 80))
                xT = self.map_x_coordinate(object.nearest[i].location[0])
                yT = self.pixel_y_max - self.map_y_coordinate(object.nearest[i].location[1])
                self.create_line(x1, y1, xT, yT, width=1, fill=color)

        if (x2 != 0 and y2 != 0):
            self.create_line(x1,y1,x2,y2, width=3, fill=object.color)
        else:
            self.create_line(x1,y1,x2,y2, width=2, fill='#999999')

        if(object.heading != 0):
            self.create_line(x1, y1, x3, y3, width=4, fill='#111111')

    def is_object_in_draw_space(self,object):
        x = self.map_x_coordinate(object.location[0])
        y = self.pixel_y_max - self.map_y_coordinate(object.location[1])

        if (x >= self.display_x_min and x <= self.display_x_max):
            if (y >= self.display_y_min and y <= self.display_y_max):
                return True

        return False

    def create_circle(self, x, y, r, color, **kwargs):
        #self.create_rectangle(x-r*6,y-r*6,x+r*6,y+r*6, fill='#444444', outline='#000000',width=2, stipple='gray75')
        return self.create_oval(x - r, y - r, x + r, y + r, fill=color, **kwargs)

    def add_object_to_draw(self,object):
        x = self.map_x_coordinate(object.location[0])
        y = self.pixel_y_max - self.map_y_coordinate(object.location[1])
        r = object.size
        c = object.color
        #print('DRAW: ',x,'\t',y)

        if(self.is_object_in_draw_space(object)):
            self.debug_overlay(object)
            self.create_circle(x,y,r,c,outline='#000000',width=2)
            if (object.needsText):
                text=(
                    "health: "+str(int(object.health))+
                    "\nfood: "+str(int(object.foodAmount))+
                    "\nimperative: "+str(object.mostImperativeIndex)
                )
                self.create_text(x, y + 2.5 * r, text=text)

    def draw_world_borders(self,worldSpace):
        x1 = self.map_x_coordinate(worldSpace[0])
        y1 = self.pixel_y_max - self.map_y_coordinate(worldSpace[1])
        x2 = self.map_x_coordinate(worldSpace[2])
        y2 = self.pixel_y_max - self.map_y_coordinate(worldSpace[3])

        self.create_line(x1, y1, x2, y1, width=10, fill='#000000')
        self.create_line(x2, y1, x2, y2, width=10, fill='#000000')
        self.create_line(x2, y2, x1, y2, width=10, fill='#000000')
        self.create_line(x1, y2, x1, y1, width=10, fill='#000000')

    def draw(self):
        tk.Canvas.update_idletasks(self)
        tk.Canvas.update(self)

    def clear(self):
        tk.Canvas.delete(self,"all")