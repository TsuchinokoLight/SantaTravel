import numpy as np


# 素数判定　マイナスは非対応
def is_prime_num(q):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q & 1 == 0: return False
    return pow(2, q - 1, q) == 1


def calc_distance(here_city, dest_city):
    here_point = np.array([here_city["X"], here_city["Y"]])
    dest_point = np.array([dest_city["X"], dest_city["Y"]])
    return np.linalg.norm(here_point - dest_point)
