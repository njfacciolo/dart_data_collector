import tkinter as tk
from tkinter import StringVar
from models.data_writer import Data_Writer
from gui.label_entry_box import Label_Entry_Box
import time
from tkinter import messagebox

class Drinks_Frame(tk.Frame, Data_Writer):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='white', *args, **kwargs)

        self.create_data_file('drinks', 'drink_log', self._get_header())

        self.drinker = None
        self.abv = None
        self.volume = None

        self.drinker = StringVar()
        self.abv = StringVar()
        self.volume = StringVar()
        self.drinker.set('')
        self.abv.set('5.0')
        self.volume.set('12.0')

        self._build_frame()


    def _build_frame(self):
        thrower_frame = Label_Entry_Box(self, bg='white')
        thrower_frame.pack()
        thrower_frame.label.configure(text='Drinker:')
        thrower_frame.entry.configure(textvariable=self.drinker)

        abv_frame = Label_Entry_Box(self, bg='white')
        abv_frame.pack()
        abv_frame.label.configure(text='ABV:')
        abv_frame.entry.configure(textvariable=self.abv)


        vol_frame = Label_Entry_Box(self, bg='white')
        vol_frame.pack()
        vol_frame.label.configure(text='Volume (oz):')
        vol_frame.entry.configure(textvariable=self.volume)

        # build the button that registers the new drink
        button = tk.Button(self, bg='white',text='Drink!', command=self._on_press)
        button.pack()


    def _get_header(self):
        return '{},{},{},{}'.format('Time', 'Thrower', 'abv', 'volume (ml)')

    def _on_press(self):
        vals = []
        vals.append(self.try_parse_string(self.drinker.get()))
        vals.append(self.try_parse_float(self.abv.get()))
        vals.append(self.try_parse_float(self.volume.get()))

        for v, succ in vals:
            if not succ:
                tk.messagebox.showerror(title='Bad Data Warning', message='Check the drinking data entry fields for mistakes')
                # print('Warning served!')
                return

        data_string = '{},{},{:.2f},{:.2f}'.format(time.time(), vals[0][0], vals[1][0], vals[2][0])
        print('Writing data: {}'.format(data_string))
        self.write_data(data_string)
        self.drinker.set('')

    def try_parse_float(self, value):
        try:
            return float(value), True
        except ValueError:
            return None, False

    def try_parse_string(self, value):
        try:
            v = str(value).strip(' ').lower()
            if v != '':
                return v, True
            else:
                return None, False
        except ValueError:
            return None, False
