import numpy as np

fast_mode = True


# 素数判定　マイナスは非対応
def is_prime_num(q):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q & 1 == 0: return False
    return pow(2, q - 1, q) == 1


def calc_distance(from_city, dest_city):
    if fast_mode is True:
        distance_x = np.abs(dest_city["X"] - from_city["X"])
        distance_y = np.abs(dest_city["Y"] - from_city["Y"])
        return distance_x + distance_y
    else:
        here_point = np.array([from_city["X"], from_city["Y"]])
        dest_point = np.array([dest_city["X"], dest_city["Y"]])
        return np.linalg.norm(here_point - dest_point)
