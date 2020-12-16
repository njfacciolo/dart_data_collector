import sys
import os

DATA_BASE = os.getcwd() + "//data//"



class Throw:
    data_folder = ""
    data_file = ""

    @staticmethod
    def create_data_file(file_name, game_type):
        if game_type == 'cricket':
            Throw.data_folder = DATA_BASE + 'cricket_games'
        else:
            Throw.data_folder = DATA_BASE + 'data_points'

        Throw.data_file = file_name + '.csv'

        Throw.write_data("Time,Thrower,Sector,Multiplier,Drinks,RawPoint")

    @staticmethod
    def write_data(line):
        with open(Throw.data_folder + Throw.data_file) as data:
            data.write(line + "\n")

    def __init__(self):
        self.time = 0
        self.thrower = ''
        self.location = (0,0)
        self.point_value = 0
        self.multiplier = 0
        self.number_of_drinks = 0

    def store_throw(self):
        csv = '{},{},{},{},{},{}'.format(self.time, self.thrower, self.point_value, self.multiplier, self.number_of_drinks, self.location)
        Throw.write_data(csv)

    def set_time(self, time):
        self.time = time

    def set_thrower(self, thrower):
        self.thrower = thrower

    def set_location(self, location):
        self.location = location

    def set_point(self, point_value):
        self.point_value = point_value

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier

    def set_num_drinks(self, drinks):
        self.number_of_drinks = drinks

