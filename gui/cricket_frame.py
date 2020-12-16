import tkinter as tk
from tkinter import ttk

class Cricket_Frame(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master


