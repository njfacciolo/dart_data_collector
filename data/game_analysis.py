import bisect
from datetime import datetime, timedelta, timezone
import os
import numpy as np
from gui.cricket_ordered_frame import Ordered_Cricket
from data.geometry_util import deg2rad, pol2cart
from collections import defaultdict
import math
from data.parse_util import try_parse_float, try_parse_string
from models.throw import Throw
from data import throw_util, drink_util
from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points
import gui.configuration as CONFIG

POLYGONS = {}

class Ordered_Cricket_Analysis():
    def __init__(self, analyzed_throws):
        self.throws = analyzed_throws
        self.player_name = analyzed_throws[0].thrower_name
        self.num_throws = len(analyzed_throws)

        # key 0 is a quick lookup for all throws\

        # series of 1s and 0s where 1 is a hit and 0 is a miss
        self._hits = defaultdict(lambda : [])

        # distance of miss
        self._miss_distance = defaultdict(lambda : [])

        # smallest x y delta to hit
        self._correction_to_hit = defaultdict(lambda : [])

        self.average_num_drinks = 0

        #initialize the full set series
        self._hits[0]=[]
        self._miss_distance[0]=[]
        self._correction_to_hit[0]=[]




    def analyze(self):
        if self.throws is None:
            return

        drinks = []

        for throw in self.throws:
            drinks.append(throw.number_of_drinks)

            v = throw.target_value
            self._hits[v].append(1 if v == throw.point_value else 0)

            miss_delta = (throw.nearest_coord_in_target[0] - throw.cartesian_x, throw.nearest_coord_in_target[1] - throw.cartesian_y,)
            self._correction_to_hit[v].append(miss_delta)

            self._miss_distance[v].append( Point(0,0).distance(Point(miss_delta)))

        # Aggregate all data for convenience
        for key in self._hits:
            self._hits[0].extend(self._hits[key])
            self._miss_distance[0].extend(self._miss_distance[key])
            self._correction_to_hit[0].extend(self._correction_to_hit[key])

        return

def analyze_game_ordered_cricket(throw_dic, drink_dic):
    # for thrower in dict
    # for throw in throws
    # set throw target
    # calculate accuracy of throw
    # apply num drinks at toss
    # store data

    # create a dummy game for tracking scores
    dummy_game = Ordered_Cricket(player_count=2)

    analysis_list = []

    for i, thrower in enumerate(throw_dic):
        if thrower not in drink_dic:
            print('Failed to find drink data for {}.'.format(thrower))
            drink_dic[thrower] = ((datetime.now(), 0.0))
        for throw in throw_dic[thrower]:
            throw.thrower = i
            throw.number_of_drinks = calculate_drinks_at_time(throw.time, drink_dic[thrower])
            throw.target_value = dummy_game.get_thrower_target(i)
            throw.nearest_coord_in_target = calculate_nearest_coord_in_target(throw)
            dummy_game.add_throw(throw)

        # Create a new analysis with the data
        analysis_list.append( Ordered_Cricket_Analysis(throw_dic[thrower]))
    for oca in analysis_list:
        oca.analyze()

    # visualize info?


def calculate_drinks_at_time(time, drink_data):
    if time is None or drink_data is None or drink_data is []:
        return 0.0

    if len(drink_data) is 1:
        return drink_data[0][1]

    # drink data is in format (time, num drinks)
    to_insert = (time,-1.0)
    index = bisect.bisect_left(drink_data, to_insert)

    if index == 0:
        return drink_data[0][1]

    if index >= len(drink_data):
        return drink_data[-1][1]

    # Perform linear approximation
    p1, p2 = drink_data[index-1], drink_data[index]
    t1, t2 = p1[0], p2[1]

    slope = (p2[1]-p1[1]) / (p2[0]-p1[0]).total_seconds()
    dt = (time-t1).total_seconds()
    aproximation = slope*dt + p1[1]
    return aproximation

def calculate_nearest_coord_in_target(throw):
    target_polygon = get_polygon(throw.target_value)
    point = Point(throw.cartesian_x, throw.cartesian_y)
    if point.within(target_polygon):
        return point.x, point.y

    # nearest point returns the nearest point in both geometries. This always returns point as p2. Unused
    poly_point, p2 = nearest_points(target_polygon, point)

    return poly_point.x, poly_point.y

def get_polygon(value):
    if value not in POLYGONS:
        POLYGONS[value] = _build_polygon(value)

    return POLYGONS[value]

def _build_polygon(value):
    scaling_ratio = CONFIG.DISPLAY_BOARD_SIZE[0] / CONFIG.DARTBOARD_IMAGE_DIMENSIONS[0]
    outter_radius = CONFIG.DIAMETERS[-1] * scaling_ratio

    arc_segments = 150
    # start with getting the swept angle based on the target point value
    value_list = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]

    # special case, return a circle
    if 25 not in POLYGONS:
        POLYGONS[25] = Point(0, 0).buffer(CONFIG.DIAMETERS[1] * scaling_ratio)

    if value == 25:
        return POLYGONS[25]

    bulls = POLYGONS[25]

    wedge_exterior_pts = []
    wedge_exterior_pts.append([0,0])

    theta1_deg = (value_list.index(value) * (18))-9
    theta2_deg = theta1_deg+18

    t1 = deg2rad(theta1_deg)
    t2 = deg2rad(theta2_deg)
    for theta in np.linspace(t1, t2, 32):
        x,y = pol2cart(outter_radius, theta)
        wedge_exterior_pts.append([x,y])

    # Generate a full slice of pie between center point and outter radius
    pie = Polygon(wedge_exterior_pts)

    # Chop off the interior bit that overlaps with the bullseye
    ret = pie.difference(bulls)
    return ret

if __name__ == "__main__":
    path = os.getcwd() + '//data_points//2020-12-18 23.56.38.csv'

    _build_polygon(6)


    throw_dic = throw_util.load_game(path)
    game_start_time = None
    for key in throw_dic:
        if game_start_time is None or throw_dic[key][0].time < game_start_time:
            game_start_time = throw_dic[key][0].time

    n_drink_curve = drink_util.generate_dummy_drink_data('n', game_start_time)
    c_drink_curve = drink_util.generate_dummy_drink_data('c', game_start_time)
    drink_dic = {}
    drink_dic['n'] = n_drink_curve
    drink_dic['c'] = c_drink_curve

    analyze_game_ordered_cricket(throw_dic, drink_dic)