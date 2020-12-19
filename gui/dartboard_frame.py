import os
import bisect
import tkinter as tk
import cv2
import numpy as np
import math
from models.throw import Throw
from PIL import Image, ImageTk
from gui import configuration as CONFIG

images_dir = os.getcwd() + '//gui//images//'
board_dims = CONFIG.DISPLAY_BOARD_SIZE

#full image measurements
center = CONFIG.CENTER
diameters = CONFIG.DIAMETERS
draw_overlay = CONFIG.DRAW_OVERLAY

class Dartboard_Frame(tk.Frame):

    def __init__(self, master=None, game_controller=None, *args, **kwargs):
        tk.Frame.__init__(self, master, background='white', *args, **kwargs)

        # This is the tkinter canvas object
        self.board = None
        self.controller = game_controller

        self.scores = []
        self.multipliers = []
        self.scale = 0
        self.darts_on_board = []

        # Numpy images
        self.np_blank_dartboard = cv2.imread(images_dir + 'dartboard.png')
        self.np_blank_dartboard = cv2.cvtColor(self.np_blank_dartboard, cv2.COLOR_RGB2BGR)
        self.scale = board_dims[0] / self.np_blank_dartboard.shape[0]
        self.np_blank_dartboard = cv2.resize(self.np_blank_dartboard, board_dims)

        # Convenient offsets
        self.cx = round(center[0] * self.scale)
        self.cy = round(center[1] * self.scale)
        self.c = (int(self.cx), int(self.cy))

        # Overlay of quadrants on undrlying image
        if draw_overlay:
            self.np_blank_dartboard = self._draw_overlay_definition()

        # Clone and build the current board
        self.np_current_board = self.np_blank_dartboard.copy()
        self.tk_current_board = None

        self._build_frame()
        self._update_frame()

        # self._overlay_definition()
        self._build_scoring_table()

    def _build_frame(self):
        self.board = tk.Canvas(self, bg='white', height=board_dims[0], width=board_dims[1])
        self.board.pack()

        # bindings for mouse clicks
        # mouseclick event
        self.board.bind("<Button 1>", self._on_click)
        # mouseclick event
        self.board.bind("<Button 3>", self._on_click_undo)

    def _update_frame(self):
        self.tk_current_board = self._create_image(self.np_current_board)
        x,y = board_dims
        self.board.create_image(int(x/2),int(y/2), anchor=tk.CENTER, image=self.tk_current_board)

    def _create_image(self, image):
        return ImageTk.PhotoImage(image=Image.fromarray(image), width=board_dims[0], height=board_dims[1])

    def _reset_display(self, event=None):
        self.darts_on_board = []
        self._draw_current_board()
        self._update_frame()

    def _draw_overlay_definition(self):
        #Useful for validating board definition
        out = self.np_blank_dartboard.copy()
        for d in diameters:
            out = cv2.circle(out, self.c, int(round(d * self.scale/2)), (255,0,0), 1)

        for a in range(9, 360, 18):
            r = (diameters[len(diameters)-1]/2) *1.1*self.scale
            r = int(round(r))

            x, y = pol2cart(r, deg2rad(a))
            p2 = (round(int(y+self.cy)), round(int(x+self.cx)))
            out = cv2.line(out, self.c, p2, (255,0,0), 1)

        return out

    def _draw_current_board(self):
        img = self.np_blank_dartboard.copy()
        for i, throw in enumerate(self.darts_on_board):
            #Convert back to abosulte units
            x = throw.cartesian_x + self.c[0]
            y = -1 * (throw.cartesian_y - self.c[1])
            v = throw.point_value
            m = throw.multiplier

            # Overlay a circle where the dart landed
            img = cv2.circle(img, (x,y), 2, (0,0,255), -1)

            # Overlay info about the point next to the dart
            img = cv2.putText(img, str(v) + ', ' + str(m), (x+5, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), lineType=cv2.LINE_AA)

            # Print the same info as above in top left
            img = cv2.putText(img, str(v) + ', ' + str(m), (20, 30 + (i * 20)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), lineType=cv2.LINE_AA)

        self.np_current_board = img

    def _build_scoring_table(self):
        self.scores = []
        self.multipliers = []

        # start with getting the points based on the angle
        value_list = [6,13,4,18,1,20,5,12,9,14,11,8,16,7,19,3,17,2,15,10,6]

        for a, v in zip(range(9, 370, 18), value_list):
            angle = deg2rad(a )
            self.scores.append((angle,v))


        mult_list = [2,1,1,3,1,2,0]
        for diam, m in zip(diameters, mult_list):
            r = diam*self.scale/2
            self.multipliers.append((r,m))

        # print(self.scores)
        # print(self.multipliers)

    def coords2points(self, x, y):
        # x and y are pixel values with respect to the bullseye = 0,0
        # returns (raw_point_value, multiplier)
        radius, angle = cart2pol(x, y)

        while angle < 0:
            angle += math.pi * 2

        #check for bullseye
        mult = bisect.bisect_left(self.multipliers, (radius, 0))
        if mult == 0:
            return 25, 2
        if mult == 1:
            return 25, 1
        if mult >= len(self.multipliers):
            return 0,0

        multiplier = self.multipliers[mult][1]

        key = bisect.bisect_left(self.scores, (angle, 0))

        return self.scores[key][1], multiplier

    def _set_throw_location(self, throw, event):
        raw_x = event.x
        raw_y = event.y

        x = raw_x - self.c[0]
        y = -1 * (raw_y - self.c[1])
        r,t = cart2pol(x,y)
        throw.set_location(x,y,r,t)

    def _on_click(self, event):
        if len(self.darts_on_board) >= 3:
            self._confirm_board()
            self._reset_display()
            return

        #Create a new Throw event
        throw = Throw()
        self._set_throw_location(throw, event)
        p,m = self.coords2points(throw.cartesian_x, throw.cartesian_y)
        throw.set_point_value(p)
        throw.set_multiplier(m)

        self.darts_on_board.append(throw)
        self._draw_current_board()
        self._update_frame()

    def _on_click_undo(self, event = None):
        if len(self.darts_on_board) > 0:
            self.darts_on_board.pop()

        self._draw_current_board()
        self._update_frame()

    def _confirm_board(self):
        self.controller.handle_new_throws(self.darts_on_board)




def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

def deg2rad(deg):
    return deg * (math.pi)/(180)

def rad2deg(rad):
    return rad * (180)/(math.pi)



if __name__ == "__main__":
    window = tk.Tk()
    frame = Dartboard_Frame(window)
    frame.pack()
    window.mainloop()