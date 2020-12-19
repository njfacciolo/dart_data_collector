import tkinter as tk
from gui.score_frame import Score_Frame
from gui.score_header_frame import Score_Header_Frame
from models.data_writer import Data_Writer
from models.game_state import Game_State


class Ordered_Cricket(Game_State):
    def __init__(self, player_count):
        Game_State.__init__(self, player_count, 3)
        self.valid_throws = [x for x in range(20,14,-1)]
        self.valid_throws.append(25)

    def add_throw(self, throw):
        if not throw.point_value in self.valid_throws:
            return '0'

        score = self.states[throw.thrower]
        for valid_throw in self.valid_throws:
            if throw.point_value == valid_throw:
                return self.update_state(throw)
            if not score.is_closed(valid_throw):
                return '0'

    def is_game_over(self):
        all_closed = True
        for state in self.states:
            for v in self.valid_throws:
                if not state.is_closed(v):
                    all_closed = False
                    break
        if all_closed:
            return True
        return False

    def is_thrower_done(self, thrower):
        for v in self.valid_throws:
            if not self.states[thrower].is_closed(v):
                return False
        return True

    def reset_game(self):
        self._reset_game()


class Cricket_Ordered_Frame(tk.Frame, Data_Writer, Ordered_Cricket):
    def __init__(self, master=None, controller=None, *args, **kwargs):
        tk.Frame.__init__(self, master, bg='white', *args, **kwargs)
        Ordered_Cricket.__init__(self, 2)
        Data_Writer.__init__(self)


        self.current_thrower = 0
        self.dart_controller = controller
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
        if self.data_file == None:
            self.create_data_file('data_points')

        for throw in throws:
            throw.thrower = self.current_thrower
            throw.thrower_name = self.header.ent1.get() if self.current_thrower == 0 else self.header.ent2.get()
            self.write_data(throw.get_data_string())

            new_val = self.add_throw(throw)
            #update board
            self._update_score_board(throw, new_val)

            #check if the game has been won
            if self.is_game_over():
                return True

            if self.is_thrower_done(self.current_thrower):
                break

        self.current_thrower = (self.current_thrower + 1) % 2
        if self.is_thrower_done(self.current_thrower):
            self.current_thrower = (self.current_thrower + 1) % 2

        self._update_thrower()
        return False

    def _update_score_board(self, throw, image):
        key = 'B' if throw.point_value == 25 else str(throw.point_value)
        if key not in self.score_frames:
            return
        frame = self.score_frames[key]
        frame.set_score(throw.thrower, image)

        self.header.set_score(throw.thrower, self.states[throw.thrower].score)

    def _reset_score_board(self):
        self.reset_game()
        for player in range(self.player_count):
            self.header.set_score(player, 0)
            for score_frame in self.score_frames:
                self.score_frames[score_frame].set_score(player, '0')

        self.current_thrower = 0
        self._update_thrower()

        # Reset data tracking
        self.data_file = None
        self.data_folder = None

    def _update_thrower(self):
        self.header.set_thrower(self.current_thrower)



if __name__ == "__main__":
    window = tk.Tk()
    window.configure(bg='white')
    window.title("Dart Data Collection")
    frame = Cricket_Ordered_Frame(window)
    frame.pack()

    window.mainloop()


