import numpy as np

fast_mode = True


# 素数判定　マイナスは非対応
def is_prime_num(q):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q & 1 == 0: return False
    return pow(2, q - 1, q) == 1


def calc_distance(from_x, from_y, dest_x, dest_y):
    distance_x = np.abs(dest_x - from_x)
    distance_y = np.abs(dest_y - from_y)
    return distance_x + distance_y


def value2coordinate(value):
    return int(round(value))
