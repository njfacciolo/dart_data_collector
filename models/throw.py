import sys
import os
import time




class Throw:
    angularOffset = 0
    radiuses = []

    @staticmethod
    def get_data_format():
        return "Time,Thrower,Sector,Multiplier,Drinks,RawX,RawY,PolarRadius,PolarAngle"

    def set_calibration_(self, angular_offset, radiuses ):
        Throw.angularOffset = angular_offset
        Throw.radiuses = radiuses


    def __init__(self):
        self.time = time.time()
        self.thrower = ''
        self.thrower_name = ''

        # values are based around the board origin at 0,0
        self.cartesian_x = 0
        self.cartesian_y = 0
        self.polar_radius = 0
        self.polar_theta = 0

        self.point_value = 0
        self.multiplier = 0
        self.number_of_drinks = 0

    def get_data_string(self):
        csv = '{},{},{},{},{},{},{},{},{}'.format(self.time, self.thrower_name, self.point_value, self.multiplier, self.number_of_drinks, self.cartesian_x, self.cartesian_y, self.polar_radius, self.polar_theta)
        return csv

    def set_thrower(self, thrower):
        self.thrower = thrower

    def set_thrower_name(self, name):
        self.thrower_name = name


    def set_location(self, cartx, carty, polr, pola):
        self.cartesian_x = cartx
        self.cartesian_y = carty
        self.polar_radius = polr
        self.polar_theta = pola

    def set_point_value(self, point):
        self.point_value = point

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier

    def set_num_drinks(self, drinks):
        self.number_of_drinks = drinks

