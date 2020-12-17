import tkinter as tk
from tkinter import ttk
from gui.dartboard_frame import Dartboard_Frame
from gui.cricket_frame import Cricket_Frame

class Darts_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.current_game = None


        self._build_window()

    def _build_window(self):
        self.title('Darrrrrts')

        game_window = ttk.Notebook(self)
        game_window.pack(side='left', fill='y')

        cricket_frame = Cricket_Frame(game_window)
        game_window.add(cricket_frame, text='Cricket')

        data_frame = tk.Frame(master=game_window, width=100, height=100)
        game_window.add(data_frame, text='Data')
        game_window.select(cricket_frame)
        game_window.enable_traversal()

        dartboard = Dartboard_Frame(master = self, game=cricket_frame)
        dartboard.pack()