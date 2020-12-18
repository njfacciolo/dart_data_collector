import os
import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk

images_dir = os.getcwd() + '//gui//images//'
row_score_size = (60,60)

class Score_Frame(tk.Frame):
    score_images = None

    def __init__(self, master=None, point_value=None, *args, **kwargs):
        tk.Frame.__init__(self, master, background='white', *args, **kwargs)

        self.master = master
        self.point_value = point_value

        if Score_Frame.score_images is None:
            self._load_score_images()

        self.p1 = None
        self.p1_image = None
        self.p2 = None
        self.p2_image = None
        self._build_frame()

    def _load_score_images(self):
        Score_Frame.score_images = {}
        Score_Frame.score_images['0'] = cv2.imread(images_dir + '0.png')
        Score_Frame.score_images['1'] = cv2.imread(images_dir + '1.png')
        Score_Frame.score_images['2'] = cv2.imread(images_dir + '2.png')
        Score_Frame.score_images['3_1'] = cv2.imread(images_dir + '3_1.png')
        Score_Frame.score_images['3_2'] = cv2.imread(images_dir + '3_2.png')
        Score_Frame.score_images['3_3'] = cv2.imread(images_dir + '3_3.png')

        #Resize the images to a more apropriate scale
        for name in Score_Frame.score_images:
            Score_Frame.score_images[name] = cv2.resize(Score_Frame.score_images[name], row_score_size, interpolation=cv2.INTER_AREA)

    def _build_frame(self):
        self.p1_image = self._create_image(Score_Frame.score_images['0'])
        self.p2_image = self._create_image(Score_Frame.score_images['0'])

        self.p1 = tk.Label(self, compound=CENTER, image=self.p1_image, background='white')
        self.p1.pack(side='left')

        score_indicator = tk.Label(self, text=' {} '.format(self.point_value), font = 'helvetica 24', bg='white')
        score_indicator.pack(side='left')

        self.p2 = tk.Label(self, compound=CENTER, image=self.p2_image, background='white')
        self.p2.pack(side='left')

    def _create_image(self, image):
        return ImageTk.PhotoImage(image=Image.fromarray(image), width=row_score_size[0], height=row_score_size[1])


    def set_score(self, player, score):
        assert score in Score_Frame.score_images

        if player == 0:
            self.p1_image = self._create_image(Score_Frame.score_images[score])
            self.p1.config(image=self.p1_image)
        else:
            self.p2_image = self._create_image(Score_Frame.score_images[score])
            self.p2.config(image=self.p2_image)



if __name__ == "__main__":
    window = tk.Tk()
    frame = Score_Frame(window, point_value=20)
    frame.pack()
    window.mainloop()

