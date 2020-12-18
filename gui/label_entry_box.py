import tkinter as tk

class Label_Entry_Box(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.label = tk.Label(self,*args, **kwargs)
        self.label.pack(side='left')
        self.entry = tk.Entry(self,*args, **kwargs)
        self.entry.pack(side='left')

