import csv
import os
import sys
from throw import Throw
from datetime import  datetime



class Data_Writer:
    def __init__(self):
        self.data_folder = None
        self.data_file = None

    def create_data_file(self, game_type, file_name = None):
        self.data_folder = os.getcwd() + "//data//"
        self.data_folder += 'cricket_games//' if game_type == 'cricket' else 'data_points//'

        if file_name is None:
            file_name = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        self.data_file = file_name + ".csv"

        # Write the header for the incoming data
        self.write_data(Throw.get_data_format())

    def write_data(self, to_write):
        with open(self.data_folder + self.data_file, 'a') as data:
            data.write(to_write + "\n")