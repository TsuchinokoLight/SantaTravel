import pandas as pd
import numpy as np
from util import value2coordinate
import math

MOVE_DOWN = 2
MOVE_UP = 8
MOVE_RIGHT = 6
MOVE_LEFT = 4

K_NN_NUM = 3


SEARCH_RANGE = 1000

class CityExplorer:
    def __init__(self, img, rest_city_df):
        self.near_cities = []
        self.rest_city_df = rest_city_df
        self.img = img
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        self.cursor_x = 0
        self.cursor_y = 0
        self.found_counter = K_NN_NUM

    def __find_mahalanobis_near(self, from_here):
        # return city index
        return 0

    def __reset_found_counter(self, found_counter):
        # 探索数（# k-Nearest Neighbor）
        if found_counter <= 0:
            # 残りの街が存在しないときは終了
            found_counter = 0
        elif found_counter >= K_NN_NUM:
            found_counter = K_NN_NUM
        return found_counter

    def __reset_over_y(self, cursor_y):
        if self.rows <= cursor_y:
            cursor_y = self.rows - 1
        elif cursor_y < 0:
            cursor_y = 0
        return cursor_y

    def __reset_over_x(self, cursor_x):
        if self.cols <= cursor_x:
            cursor_x = self.cols - 1
        elif cursor_x < 0:
            cursor_x = 0
        return cursor_x

    def __xy2city_id(self, x, y):
        x_arr = self.rest_city_df["X"].values
        y_arr = self.rest_city_df["Y"].values
        id_arr = []

        for index in range(self.rest_city_df.shape[0]):
            if value2coordinate(x_arr[index]) == x and value2coordinate(y_arr[index]) == y:
                id_arr.append(self.rest_city_df.iloc[index])
        return id_arr

    def __add_cursor_city(self):
        # ・self.rest_city_df[ID(INDEX)指定]
        # ・今持っている情報は、X,Yの情報
        # ・self.imgの値はIDの総和
        # ・rest_city_dfから見つけたら、img-IDを行う
        # ・とりあえず、X,Y→ID変換を行う

        #candidates_x = self.rest_city_df[(self.cursor_x <= self.rest_city_df["X"]) & (self.rest_city_df["X"] < self.cursor_x + 1)]
        #target_cities = candidates_x[(self.cursor_y <= candidates_x["Y"]) & (candidates_x["Y"] < self.cursor_y + 1)]

        count = 0
        target_cities = self.__xy2city_id(self.cursor_x, self.cursor_y)
        if target_cities is None:
            return 0
        for target_city in target_cities:
            # 同じ座標に複数の街がある場合を考慮してループ
            self.near_cities.append(target_city)
            self.found_counter = self.found_counter - 1
            count = count + 1
            if self.found_counter <= 0:
                # 一定数になったら終了
                break

        return count

    def __findmove_x(self, step, length):
        for move_cnt in range(length):
            # 街があるか確認
            if self.img[self.cursor_y, self.cursor_x] > 0:
                self.__add_cursor_city()
                if self.found_counter <= 0:
                    # 一定数になったら終了
                    return self.found_counter
            # 移動
            self.cursor_x = self.__reset_over_x(self.cursor_x + step)

        return self.found_counter

    def __findmove_y(self, step, height):
        for move_cnt in range(height):
            # 街があるか確認
            if self.img[self.cursor_y, self.cursor_x] > 0:
                self.__add_cursor_city()
                if self.found_counter <= 0:
                    # 一定数になったら終了
                    return self.found_counter
            # 移動
            self.cursor_y = self.__reset_over_y(self.cursor_y + step)

        return self.found_counter

    def __findmove(self, direction, move_cnt):
        if direction == MOVE_DOWN:
            return self.__findmove_y(step=1, height=move_cnt)
        elif direction == MOVE_UP:
            return self.__findmove_y(step=-1, height=move_cnt)
        elif direction == MOVE_RIGHT:
            return self.__findmove_x(step=1, length=move_cnt)
        elif direction == MOVE_LEFT:
            return self.__findmove_x(step=-1, length=move_cnt)
        else:
            print("Direction ERROR")
            return 0

    def find_eucledean_near(self, from_city):
        # 探索
        from_x = value2coordinate(from_city["X"])
        from_y = value2coordinate(from_city["Y"])

        self.found_counter = self.__reset_found_counter(self.rest_city_df.shape[0])
        window_side = 1

        while window_side * 2 < self.rows and window_side * 2 < self.cols:
            if window_side > SEARCH_RANGE:
                # ここまでくると処理が遅いので、ワープ
                warp_city = self.rest_city_df.loc[0]
                self.near_cities.append(warp_city)
                break

            # set start point
            self.cursor_x = math.floor(from_x - window_side / 2)  # 小数切り捨て
            self.cursor_x = self.__reset_over_x(self.cursor_x)  # 端っこ超えている場合は再セット
            self.cursor_y = math.floor(from_y - window_side / 2)
            self.cursor_y = self.__reset_over_y(self.cursor_y)

            # →
            self.__findmove(MOVE_RIGHT, window_side)
            if self.found_counter <= 0:
                break

            # ↓
            self.__findmove(MOVE_DOWN, window_side)
            if self.found_counter <= 0:
                break

            # ←
            self.__findmove(MOVE_LEFT, window_side)
            if self.found_counter <= 0:
                break

            # ↑
            self.__findmove(MOVE_UP, window_side)
            if self.found_counter <= 0:
                break

            window_side = window_side + 2

        return self.near_cities
