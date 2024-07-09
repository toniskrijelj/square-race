import math
import numpy as np


def move(pos, angle, unit):
    x, y = pos
    rad = math.radians(angle % 360)
    x += unit * math.cos(rad)
    y += unit * math.sin(rad)
    return x, y


def sigmoid(z):
    res = [[]]
    for v in z[0]:
        v = max(v, -500)
        v = min(v, 500)
        res[0].append(1.0 / (1.0 + np.exp(-v)))
    return res


def distance(pos, pos2):
    x, y = pos
    x2, y2 = pos2
    return ((x-x2)**2+(y-y2)**2)**0.5