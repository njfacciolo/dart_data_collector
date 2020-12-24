import bisect
import os
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points

import gui.configuration as CONFIG
from data import throw_util, drink_util, parse_util
from data.geometry_util import deg2rad, pol2cart
from gui.cricket_ordered_frame import Ordered_Cricket
from models.throw import Throw
from random import random
import math


POLYGONS = {}
NUMBER_OF_BINS = 15


class Ordered_Cricket_Analysis:
    plots = []

    @staticmethod
    def merge_data(analysis_list):
        ret = Ordered_Cricket_Analysis()
        for anal in analysis_list:
            ret.merge(anal)
        ret.analyze()
        return ret

    def __init__(self, analyzed_throws=None):
        if analyzed_throws == [] or analyzed_throws is None:
            self.throws = []
            self.player_name = ''
            self.num_throws = 0
        else:
            self.throws = analyzed_throws
            self.player_name =  analyzed_throws[0].thrower_name
            self.num_throws = len(analyzed_throws)


        # key 0 is a quick lookup for all throws\

        # series of 1s and 0s where 1 is a hit and 0 is a miss
        self.hits = defaultdict(lambda : [])

        # distance of miss
        self.miss_distance = defaultdict(lambda : [])

        # smallest x y delta to hit
        self.correction_to_hit = defaultdict(lambda : [])

        self.average_num_drinks = 0

        #initialize the full set series
        self.hits[0]=[]
        self.miss_distance[0]=[]
        self.correction_to_hit[0]=[]

    def merge(self, analysis):
        self.throws.extend(analysis.throws)
        if self.player_name == '':
            self.player_name = self.throws[0].thrower_name
        self.num_throws = len(self.throws)

    def analyze(self):
        if self.throws is None:
            return

        drinks = []

        for throw in self.throws:
            drinks.append(throw.number_of_drinks)

            v = throw.target_value
            self.hits[v].append(1 if v == throw.point_value else 0)

            miss_delta = (throw.nearest_coord_in_target[0] - throw.cartesian_x, throw.nearest_coord_in_target[1] - throw.cartesian_y,)
            self.correction_to_hit[v].append(miss_delta)

            miss_distance = Point(0, 0).distance(Point(miss_delta))
            self.miss_distance[v].append(miss_distance)
            throw.miss_distance = miss_distance

        self.average_num_drinks = np.average(drinks)

        # Aggregate all data for convenience
        for key in self.hits:
            self.hits[0].extend(self.hits[key])
            self.miss_distance[0].extend(self.miss_distance[key])
            self.correction_to_hit[0].extend(self.correction_to_hit[key])

        return

    def plot_throw_data(self):
        x, y = [throw.number_of_drinks for throw in self.throws], [throw.miss_distance for throw in self.throws]

        max_drinks = math.ceil((max(self.throws, key=lambda x: x.number_of_drinks)).number_of_drinks)

        # If we haven't been drinking, this doesn't really matter
        if max_drinks != 0:
            bins = np.linspace(0, max_drinks, NUMBER_OF_BINS)

            # Sort the data into appropriate bins
            data_dic = defaultdict(lambda: [])
            for throw in self.throws:
                idx = bisect.bisect_left(bins, throw.number_of_drinks)
                if idx == 0 or idx == 1:
                    data_dic[bins[0]].append(throw.miss_distance)
                else:
                    data_dic[idx - 1].append(throw.miss_distance)

            # Calculate average accuracy for each bin
            y = []
            for i, key in enumerate(bins):
                data = data_dic[i]
                if len(data) == 0:
                    y.append(0)
                else:
                    y.append(np.average(data))

            # Plot the data in a line graph
            Ordered_Cricket_Analysis.plots.append(plt.plot(bins, y, label=self.player_name))
            return

        Ordered_Cricket_Analysis.plots.append(plt.plot(x, y, label=self.player_name))
        return

    @staticmethod
    def show_plots():
        plt.ion()
        plt.title('Accuracy vs Number of Drinks')
        plt.xlabel('Number Of Drinks')
        plt.ylabel('Average Distance to Target (mm)')
        plt.legend()
        # plt.show(block=True)
        plt.show()
        Ordered_Cricket_Analysis.plots = []

def analyze_day_ordered_cricket(time=datetime.now()):
    # list of dictionaries. Each dictionary should have two entries - one for each player in game
    target_dir = os.getcwd() + '//data//data_points//'
    games = throw_util.load_days_games(os.getcwd() + '//data//data_points//', time)
    # games = throw_util.load_days_games(os.getcwd() + '//data_points//', time)

    if games == None or len(games) == 0:
        print('Found no games in {} on {}'.format(target_dir, time))
        return

    # Store the player names for future use
    players = []

    for game in games:
        if game is None:
            continue

        for player_id in game.keys():
            if game[player_id][0].thrower_name not in players:
                players.append(game[player_id][0].thrower_name)

    drink_dic = drink_util.load_daily_drinks(os.getcwd() + '//data//drinks//drink_log.csv', drinkers=players)
    # drink_dic = drink_util.load_daily_drinks(os.getcwd() + '//drinks//drink_log.csv', players)

    drink_curves = {}
    for drinker in drink_dic:
        drink_curves[drinker] = drink_util.calculate_bac_curve(drink_dic[drinker])

    # print('Analyzing drink data for {}'.format(drink_curves.keys()))

    analyzed_games = []
    for game in games:
        analyzed_games.extend(set_all_throw_details(game, drink_curves))

    merged_data = {}
    for player in players:
        merged_data[player] = Ordered_Cricket_Analysis.merge_data([game for game in analyzed_games if game.player_name == player])
        merged_data[player].analyze()
        merged_data[player].plot_throw_data()

    Ordered_Cricket_Analysis.show_plots()
    return

def analyze_game_ordered_cricket(game_path):
    if not os.path.exists(game_path):
        print('Failed to find game at location: {}  Skipping game analysis...'.format(game_path))
        return

    throw_dic = throw_util.load_game(game_path)
    date = datetime.strptime((parse_util.path_leaf(game_path)).strip('.csv'), '%Y-%m-%d %H.%M.%S')

    drink_dic = drink_util.load_daily_drinks(os.getcwd() +'//data//drinks//drink_log.csv', time=date)
    drink_curves = {}
    for drinker in drink_dic:
        drink_curves[drinker] = drink_util.calculate_bac_curve(drink_dic[drinker])

    analyze_ordered_cricket(throw_dic, drink_curves)


def analyze_ordered_cricket(throw_dic, drink_curve_dic):
    analysis = set_all_throw_details(throw_dic, drink_curve_dic)

    for anal in analysis:
        anal.analyze()

    # visualize info?
    gd1, gd2 = analysis[0], analysis[1]
    print('Stat: {}, {}'.format(gd1.player_name, gd2.player_name))
    print('Average Drinks: {:.2f}, {:.2f}'.format(gd1.average_num_drinks, gd2.average_num_drinks))
    print('Num Throws: {}, {}'.format(gd1.num_throws, gd2.num_throws))
    print('Game Average Hit Percent: {:.2f}%, {:.2f}%'.format(np.average(gd1.hits[0])*100, np.average(gd2.hits[0])*100))

    valid_throws = [20,19,18,17,16,15,25]
    for score in valid_throws:
        print('{} Hit Percent: {:.2f}%, {:.2f}%'.format(score, np.average(gd1.hits[score]) * 100,
                                                                  np.average(gd2.hits[score]) * 100))

    px2mm = CONFIG.PIXEL2MM

    print('\n')
    print('Game Average Miss Distance: {:.1f}mm, {:.1f}mm'.format(np.average(gd1.miss_distance[0]) * px2mm, np.average(gd2.miss_distance[0])*px2mm))
    for score in valid_throws:
        d1 = gd1.correction_to_hit[score]
        d2 = gd2.correction_to_hit[score]
        xavg1, yavg1 = [x[0] for x in d1 if x[0] != 0], [y[1] for y in d1 if y[0] != 0]
        xavg2, yavg2 = [x[0] for x in d2 if x[0] != 0], [y[1] for y in d2 if y[0] != 0]
        for avgs in [xavg1, yavg1, xavg2, yavg2]:
            if len(avgs) == 0:
                avgs.append(0)


        print('{} Average Miss Distance: {:.1f}mm, {:.1f}mm'.format(score, np.average(gd1.miss_distance[score]) * px2mm,
                                                                        np.average(gd2.miss_distance[score]) * px2mm))
        # print('{} {} Average Missed By: {:.1f}mm, {:.1f}mm    {} Average Missed By: {:.1f}mm, {:.1f}mm'.format(score,
        #                 gd1.player_name, np.average(xavg1) * px2mm, np.average(yavg1) * px2mm,
        #                 gd2.player_name, np.average(xavg2) * px2mm, np.average(yavg2) * px2mm))

    # analysis[0].plot_throw_data()
    # analysis[1].plot_throw_data()
    # analysis[0].show_plots()
    return

def set_all_throw_details(throw_dic, drink_curve_dic):
    # for thrower in dict
        # for throw in throws
            # set throw target
    # calculate accuracy of throw
    # apply num drinks at toss
    # store data
    # create a dummy game for tracking scores
    dummy_game = Ordered_Cricket(player_count=2)
    analysis = []

    #For each throw in the game, set the number of drinks, target value, and nearest coordinate to points
    for thrower_id in throw_dic:
        thrower = throw_dic[thrower_id][0].thrower_name
        if thrower not in drink_curve_dic:
            print('Failed to find drink data for {}.'.format(thrower))
            drink_curve_dic[thrower] = [(datetime.now(), 0.0)]
        for throw in throw_dic[thrower_id]:
            throw.number_of_drinks = calculate_drinks_at_time(throw.time, drink_curve_dic[thrower])
            throw.target_value = dummy_game.get_thrower_target(thrower_id)
            throw.nearest_coord_in_target = calculate_nearest_coord_in_target(throw)
            dummy_game.add_throw(throw)

        # Create a new analysis with the data
        analysis.append( Ordered_Cricket_Analysis(throw_dic[thrower_id]))

    return analysis

def calculate_drinks_at_time(time, drink_curve):
    if time is None or drink_curve is None or drink_curve is []:
        return 0.0

    if len(drink_curve) is 1:
        return drink_curve[0][1]

    # drink data is in format (time, num drinks)
    to_insert = (time,-1.0)
    index = bisect.bisect_left(drink_curve, to_insert)

    if index == 0:
        return drink_curve[0][1]

    if index >= len(drink_curve):
        return drink_curve[-1][1]

    # Perform linear approximation
    p1, p2 = drink_curve[index - 1], drink_curve[index]
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
    # path = os.getcwd() + '//data_points//2020-12-18 23.56.38.csv'
    #
    # throw_dic = throw_util.load_game(path)
    # game_start_time = None
    # for key in throw_dic:
    #     if game_start_time is None or throw_dic[key][0].time < game_start_time:
    #         game_start_time = throw_dic[key][0].time
    #
    # n_drink_curve = drink_util.generate_dummy_drink_data('n', game_start_time)
    # c_drink_curve = drink_util.generate_dummy_drink_data('c', game_start_time)
    # drink_dic = {}
    # drink_dic['n'] = n_drink_curve
    # drink_dic['c'] = c_drink_curve
    #
    # analyze_game_ordered_cricket(throw_dic, drink_dic)

    plt.ion()
    analyze_day_ordered_cricket()

