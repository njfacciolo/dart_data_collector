import tkinter as tk
from score_frame import Score_Frame
from score_header_frame import Score_Header_Frame
from random import randint
from throw import Throw
from data_writer import Data_Writer
from game_state import Game_State
from datetime import datetime

class Cricket(Game_State):
    def __init__(self, player_count):
        Game_State.__init__(self, player_count, 3)
        self.valid_throws = [x for x in range(15,21,1)]
        self.valid_throws.append(25)

    def add_throw(self, throw):
        if throw.point_value in self.valid_throws:
            return self.update_state(throw)
        return '0'



class Cricket_Frame(tk.Frame, Data_Writer, Cricket):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='white', *args, **kwargs)
        Cricket.__init__(self, 2)

        file_name = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        self.create_data_file(file_name , 'cricket')

        self.current_thrower = 0
        self.master = master
        self.header = None
        self.score_frames = {}
        self._build_frame()

    def _build_frame(self):
        self.header = Score_Header_Frame(self)
        self.header.pack()

        scores = [x for x in range(20,14,-1)]
        scores.append('B')

        for score in scores:
            s = str(score)
            f = Score_Frame(self, point_value=s)
            f.pack()
            self.score_frames[s] = f

    def new_throw_set(self, throws):
        for throw in throws:
            throw.thrower = self.current_thrower
            self.write_data(throw.get_data_string())
            new_val = self.add_throw(throw)

            #update board
            self._update_score_board(throw, new_val)

            #check if the game has been won
            # self._check_game_over()

        self.current_thrower = (self.current_thrower + 1) % 2

    def _update_score_board(self, throw, image):
        key = 'B' if throw.point_value == 25 else str(throw.point_value)
        if key not in self.score_frames:
            return
        frame = self.score_frames[key]
        frame.set_score(throw.thrower, image)

        self.header.set_score(throw.thrower, self.states[throw.thrower].score)




if __name__ == "__main__":
    window = tk.Tk()
    window.configure(bg='white')
    window.title("Dart Data Collection")
    frame = Cricket_Frame(window)
    frame.pack()

    window.mainloop()


