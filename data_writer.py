import csv
import os
import sys



class Data_Writer:
    data_folder = ""
    data_file = ""

    def create_data_file(self, file_name, game_type):
        self.data_folder = os.getcwd() + "//data//"
        self.data_folder += 'cricket_games//' if game_type == 'cricket' else 'data_points//'
        self.data_file = file_name + ".csv"

        self.write_data("Time,Thrower,Sector,Multiplier,Drinks,Raw X,Raw Y")

    def write_data(self, to_write):
        with open(self.data_folder + self.data_file, 'a') as data:
            data.write(to_write + "\n")