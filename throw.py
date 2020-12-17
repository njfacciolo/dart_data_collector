import sys
import os
import time




class Throw:
    def __init__(self):
        self.time = time.time()
        self.thrower = ''
        self.location = (0,0)
        self.point_value = 0
        self.multiplier = 0
        self.number_of_drinks = 0

    def get_data_string(self):
        csv = '{},{},{},{},{},{}'.format(self.time, self.thrower, self.point_value, self.multiplier, self.number_of_drinks, self.location)
        return csv

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

