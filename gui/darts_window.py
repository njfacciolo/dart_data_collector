import tkinter as tk
from tkinter import ttk
from gui.dartboard_frame import Dartboard_Frame
from gui.cricket_frame import Cricket_Frame
from gui.cricket_ordered_frame import Cricket_Ordered_Frame
from gui.drinks_frame import Drinks_Frame
from data.game_analysis import analyze_day_ordered_cricket, analyze_game_ordered_cricket
from threading import Thread
from time import sleep
from models.dummy_dart_player import take_turn
import os

DEBUGGING = False

class Darts_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.current_game = None
        self.frame_dartboard = None
        self.tabbed_frame_games = None
        self.available_games = []
        self._build_window()

        if DEBUGGING:
            self.dummy_thread = Thread(target=self._throw_randomly).start()

    def _build_window(self):
        self.title('Darrrrrts')

        self.left_panel = tk.Frame(self, bg='white')
        self.left_panel.pack(side='left', fill='y')

        self.tabbed_frame_games = ttk.Notebook(self.left_panel)
        self.tabbed_frame_games.pack(fill='y')

        self.drink_frame = Drinks_Frame(self.left_panel)
        self.drink_frame.pack()

        cricket_frame = Cricket_Frame(self.tabbed_frame_games, self)
        self.tabbed_frame_games.add(cricket_frame, text='Cricket')

        data_frame = Cricket_Ordered_Frame(master=self.tabbed_frame_games, controller=self)
        self.tabbed_frame_games.add(data_frame, text='Data')
        self.tabbed_frame_games.select(data_frame)
        self.tabbed_frame_games.enable_traversal()

        self.available_games.append(cricket_frame)
        self.available_games.append(data_frame)



        self.frame_dartboard = Dartboard_Frame(master = self, game_controller = self)
        self.frame_dartboard.pack()

    def handle_new_throws(self, throws):
        if self.current_game is None:
            current_index = self.tabbed_frame_games.index('current')
            self.current_game = self.available_games[current_index]

        game_ended = self.current_game.new_throw_set(throws)
        if game_ended:
            self.game_ended()
        return game_ended

    def game_ended(self):
        # print('Darts_Window:: The game has ended!')
        if self.current_game.game_name == 'ordered_cricket':
            analyze_game_ordered_cricket(self.current_game.data_folder+self.current_game.data_file)
            analyze_day_ordered_cricket()
        # else:
        #     analyze_game_cricket()

        # Reset the dartboard
        self.frame_dartboard._reset_display()

        # Reset the game states
        self.current_game._reset_score_board()

        # Remove the existing game from focus
        self.current_game = None



        # generate a new csv



    def _throw_randomly(self):
        sleep(1)
        game_ended = False
        file_to_delete = ''
        while not game_ended:
            game_ended = self.handle_new_throws(take_turn())

            if file_to_delete == '':
                file_to_delete = self.current_game.data_folder + self.current_game.data_file


        sleep(1)
        try:
            os.remove(file_to_delete)
        except:
            print('Failed to delete dummy data at {}'.format(file_to_delete))





