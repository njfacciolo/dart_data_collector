import numpy as np
import math

def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

def deg2rad(deg):
    return deg * (math.pi)/(180)

def rad2deg(rad):
    return rad * (180)/(math.pi)