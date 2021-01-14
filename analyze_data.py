import math
import numpy as np
import os
import sys
from data.drink_util import load_all_drinks, calculate_bac_curve
from data.throw_util import load_game
from data.game_analysis import set_all_throw_details_and_generate_game
from collections import defaultdict
import math
import bisect

class Data_Set:
    def __init__(self, game_id, throws):
        self.game_index = game_id
        self.all_throws = throws
        self.thrower_name = throws[0].thrower_name
        self.throws_at = defaultdict(lambda : 0)
        self.average_drinks = 0


    def format_row(self):
        data_points = []
        data_points.append(self.game_index)
        for i in range(20, 14, -1):
            data_points.append(self.throws_at[i])
        data_points.append(self.throws_at[25])
        data_points.append(self.throws_at[0])
        data_points.append(self.average_drinks)

        return ','.join(map(str, data_points))

    def analyze_throws(self):
        num_drinks = []
        for throw in self.all_throws:
            self.throws_at[0] += 1
            self.throws_at[throw.target_value] += 1
            num_drinks.append(throw.number_of_drinks)
        self.average_drinks = np.average(num_drinks)

def calculate_average_accuracy(throws):
    #bin all the throws
    #average each bin
    # return sorted list of tuples
    max_drink_throw = max(throws, key=lambda x: x.number_of_drinks)
    max_drinks = math.ceil(max_drink_throw.number_of_drinks)
    bins = defaultdict(lambda : [])
    sorter = []

    for i in np.arange(0, max_drinks+0.5, 0.5):
        sorter.append(i)

    for throw in throws:
        # get index
        bindex = bisect.bisect_left(sorter, throw.number_of_drinks)
        # get value
        bin = sorter[bindex]
        # add to bin
        bins[bin].append(throw)

    ret = []
    for bin in bins:
        accuracy = []
        for throw in bins[bin]:
            accuracy.append(throw.miss_distance)
        quartiles = np.quantile(accuracy, [0,.25,.5,.75, 1])
        stdev = np.std(accuracy)
        ret.append((bin, np.average(accuracy), stdev, quartiles))
    ret.sort(key=lambda x: x[0])
    return ret



if __name__ == "__main__":

    drinkers = ['c', 'n']

    drink_data_file = os.getcwd() + '//data//drinks/drink_log.csv'
    drink_data = load_all_drinks(drink_data_file, drinkers = drinkers)

    drink_curves = {}
    for drinker in drinkers:
        drink_curves[drinker] = calculate_bac_curve(drink_data[drinker])

    every_throw = {}
    data_sets = {}
    for drinker in drinkers:
        data_sets[drinker] = []
        every_throw[drinker] = []

    target_game_dir = os.getcwd() + '//data//data_points//'

    game_files = [file for file in os.listdir(target_game_dir) if file.endswith('.csv')]

    for i, path in enumerate(game_files):
        throw_dic = load_game(target_game_dir + path)
        game_details = set_all_throw_details_and_generate_game(throw_dic, drink_curves)

        for thrower_index in throw_dic:
            #check that the thrower is in our target data
            all_throws = throw_dic[thrower_index]
            if all_throws == None or all_throws == [] or len(all_throws) < 1:
                continue
            if all_throws[0].thrower_name not in drinkers:
                continue
            every_throw[all_throws[0].thrower_name].extend(all_throws)

            ds = Data_Set(i, all_throws)
            ds.analyze_throws()
            data_sets[all_throws[0].thrower_name].append(ds)
            # data_sets.append(Data_Set(1, all_throws))

    for drinker in drinkers:
        for data in data_sets[drinker]:
            print(drinker + ',' +data.format_row())

    averaged_accuracies = {}
    for drinker in drinkers:
        averaged_accuracies[drinker] = calculate_average_accuracy(every_throw[drinker])
        for bin in averaged_accuracies[drinker]:
            qs = ','.join(map(str, bin[3]))
            print('{},{},{},{},{}'.format(drinker, bin[0], bin[1], bin[2], qs))