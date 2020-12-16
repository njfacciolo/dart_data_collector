import tkinter as tk

class Cricket_Frame(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master






if __name__ == "__main__":
    window = tk.Tk()
    frame = Cricket_Frame(window)
    frame.pack()
    window.mainloop()


