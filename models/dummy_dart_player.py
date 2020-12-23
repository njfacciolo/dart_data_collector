from models.throw import  Throw
from random import random
import math
from data.geometry_util import cart2pol, deg2rad
import gui.configuration as CONFIG
import bisect


MULTIPLIERS = []
SCORES = []
diameters = CONFIG.DIAMETERS

def _build_scoring_table():

    # start with getting the points based on the angle
    value_list = [6,13,4,18,1,20,5,12,9,14,11,8,16,7,19,3,17,2,15,10,6]

    for a, v in zip(range(9, 370, 18), value_list):
        angle = deg2rad(a )
        SCORES.append((angle,v))


    mult_list = [2,1,1,3,1,2,0]
    for diam, m in zip(diameters, mult_list):
        r = diam * (1500/900)/2
        MULTIPLIERS.append((r,m))

def take_turn():
    ret = []
    for _ in range(3):
        ret.append(random_throw())
    return ret

def random_throw():
    if MULTIPLIERS == [] or SCORES == []:
        _build_scoring_table()
    # Create a new Throw event
    throw = Throw()
    throw.cartesian_x = round(random()*900)-450
    throw.cartesian_y = round(random()*900)-450

    p,m = coords2points(throw.cartesian_x, throw.cartesian_y)
    throw.set_point_value(p)
    throw.set_multiplier(m)

    return throw


def coords2points(x, y):
    # x and y are pixel values with respect to the bullseye = 0,0
    # returns (raw_point_value, multiplier)
    radius, angle = cart2pol(x, y)

    while angle < 0:
        angle += math.pi * 2

    #check for bullseye
    mult = bisect.bisect_left(MULTIPLIERS, (radius, 0))
    if mult == 0:
        return 25, 2
    if mult == 1:
        return 25, 1
    if mult >= len(MULTIPLIERS):
        return 0,0

    multiplier = MULTIPLIERS[mult][1]

    key = bisect.bisect_left(SCORES, (angle, 0))

    return SCORES[key][1], multiplier

