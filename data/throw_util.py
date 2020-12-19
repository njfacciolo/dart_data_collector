import csv
from datetime import datetime, timedelta, timezone
import os
from collections import defaultdict
from data.parse_util import try_parse_float, try_parse_string
from models.throw import Throw


def load_game(file):
    # If the file doesn't exist, return an empty dic
    ret = defaultdict(lambda: [])
    if not os.path.exists(file):
        return ret

    with open(file, 'r') as throw_data:
        firstline = True
        for row in list(csv.reader(throw_data)):
            if firstline:
                firstline = False
                continue
            throw = generate_throw_from_data(row)

            if throw is not None:
                ret[throw.thrower_name].append(throw)
            else:
                break
    return ret

def generate_throw_from_data(data):
    # Time, Thrower, sector, multiplier, drinks (unused), x, y, polar_radius, polar_angle
    float_time, success = try_parse_float(data[0].strip())
    if not success:
        return None

    t = Throw()
    time = int(float_time)

    t.time = datetime.fromtimestamp(time)
    t.thrower_name, name_parsed= try_parse_string(data[1])

    if not name_parsed:
        return None

    vals = []
    for i in range(2, len(data)):
        a, succ = try_parse_float(data[i])
        if not succ:
            return None
        vals.append(a)


    t.point_value = int(vals[0])
    t.multiplier = int(vals[1])
    t.number_of_drinks = vals[2]
    t.cartesian_x = vals[3]
    t.cartesian_y = vals[4]
    t.polar_radius = vals[5]
    t.polar_theta = vals[6]

    return t

if __name__ == "__main__":
    path = os.getcwd() + '//data_points//2020-12-18 23.56.38.csv'

    throw_dic = load_game(path)
