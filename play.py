import tkinter as tk
from tkinter import ttk
from gui.dartboard_frame import Dartboard_Frame
from gui.cricket_frame import Cricket_Frame

class Darts_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)


if __name__ == "__main__":
    # Build the window for the user
    print('Darrrrrrts in progress....')
    window = Darts_Window()
    window.title('Darrrrrts')

    game_window = ttk.Notebook(window)
    game_window.pack(side='left', fill='y')

    cricket_frame = Cricket_Frame(game_window)
    game_window.add(cricket_frame, text='Cricket')

    data_frame = tk.Frame(master=game_window, width=100, height=100)
    game_window.add(data_frame, text='Data')
    game_window.select(cricket_frame)
    game_window.enable_traversal()

    dartboard = Dartboard_Frame(master = window, game=cricket_frame)
    dartboard.pack()

    window.mainloop()

    print('Game Over :(')