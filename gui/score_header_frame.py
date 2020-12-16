import os
import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk

images_dir = os.getcwd() + '//images//'

class Score_Header_Frame(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, background='white', *args, **kwargs)

        self.ent1 = None
        self.ent2 = None

        self.score1 = None
        self.score2 = None
        self.score1_var = StringVar()
        self.score2_var = StringVar()
        self.score1_var.set('0')
        self.score2_var.set('0')

        self._build_frame()


    def _build_frame(self):
        w = 20
        top = tk.Frame(self, bg='white')
        top.pack()
        self.ent1 = tk.Entry(top, bg='white', width=w, justify=CENTER)
        self.ent1.insert(0, 'C')
        self.ent1.pack(side='left')

        self.ent2 = tk.Entry(top, bg='white', width=w, justify=CENTER)
        self.ent2.insert(0, 'N')
        self.ent2.pack(side='left')

        # set up the bottom frame for keeping the current score of the game
        bot = tk.Frame(self, bg='white')
        bot.pack()

        self.score1_var.set('100')
        self.score2_var.set('5')

        self.score1 = tk.Label(bot, bg='white', justify=CENTER, textvariable=self.score1_var, width=w-3)
        self.score1.pack(side='left')
        self.score2 = tk.Label(bot, bg='white', justify=CENTER, textvariable=self.score2_var, width=w-3)
        self.score2.pack(side='left')

    def set_score(self, player, score):
        if player == 1:
            self.score1_var = str(score)
        else:
            self.score2_var = str(score)

    def get_player_names(self):
        return self.ent1.get(), self.ent2.get()





if __name__ == "__main__":
    window = tk.Tk()
    frame = Score_Header_Frame(window)
    frame.pack()
    window.mainloop()