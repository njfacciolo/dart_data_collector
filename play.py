import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    # Build the window for the user
    print('building in progress...')
    window = tk.Tk()
    window.title('Dart Data Collection')

    game_window = ttk.Notebook(window)
    game_window.pack(side='left')

    cricket_frame = tk.Frame(master=game_window, width=100, height=100)
    game_window.add(cricket_frame, text='Cricket')

    data_frame = tk.Frame(master=game_window, width=100, height=100)
    game_window.add(data_frame, text='Data')
    game_window.select(cricket_frame)
    game_window.enable_traversal()

    dartboard = ttk.Frame(window)

    window.mainloop()

    print('Game Over :(')