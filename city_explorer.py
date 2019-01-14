from util import value2coordinate
import math
import Exceptions
import numpy as np
import pandas as pd
import scipy.spatial.distance as sci

MOVE_DOWN = 2
MOVE_UP = 8
MOVE_RIGHT = 6
MOVE_LEFT = 4

K_NN_NUM = 5


SEARCH_RANGE = 500

class CityExplorer:
    def __init__(self, img, rest_city_df):
        self.near_cities = pd.DataFrame()
        self.rest_city_df = rest_city_df
        self.img = img
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        self.cursor_x = 0
        self.cursor_y = 0
        self.found_counter = K_NN_NUM

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

    def __xy2city(self, x, y):
        x_arr = self.rest_city_df["X"].values
        y_arr = self.rest_city_df["Y"].values
        city_arr = []

        for index in range(self.rest_city_df.shape[0]):
            if value2coordinate(x_arr[index]) == x and value2coordinate(y_arr[index]) == y:
                city_arr.append(self.rest_city_df.iloc[index])
        return city_arr

    def __add_cursor_city(self):
        # ①X,Y→ID変換を行う
        # ②self.near_citiesに候補を追加

        target_cities = self.__xy2city(self.cursor_x, self.cursor_y)
        if target_cities is None:
            print("Error in __add_cursor_city: No target_cities...")
            raise Exceptions.NotFoundCityException()

        for target_city in target_cities:
            # 同じ座標に複数の街がある場合を考慮してループ
            self.near_cities = self.near_cities.append(target_city)
            self.found_counter = self.found_counter - 1
            if self.found_counter <= 0:
                # 一定数になったら終了
                break

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

    def __find_eucledean_near(self, from_city):
        # 探索
        from_x = value2coordinate(from_city["X"])
        from_y = value2coordinate(from_city["Y"])

        self.found_counter = self.__reset_found_counter(self.rest_city_df.shape[0])
        window_side = 1

        while window_side * 2 < self.rows and window_side * 2 < self.cols:
            if window_side > SEARCH_RANGE:
                # ここまでくると処理が遅いので、ワープ
                warp_city = self.rest_city_df.loc[0]
                self.near_cities = self.near_cities.append(warp_city)
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

    def __make_xy_covariance(self, xy_datas):
        # xy_datas: 2次元配列[][]
        # init.
        ROW = len(xy_datas) # データ数
        COLUMN = 2  # x,y
        # row:行,column:列,ave:平均,vcm:分散共分散行列
        row = []
        column = []
        ave = [0.0 for i in range(ROW)]
        vcm = np.zeros((COLUMN, ROW, ROW))
        diff = np.zeros((1, ROW))
        mahal = np.zeros(COLUMN)
        tmp = np.zeros(ROW)

        # rowにtrans_dataの要素をリストの形式で連結
        for i in range(ROW):
            row.append(xy_datas[i])
        print(row)

        # 列を連結
        for i in range(1, COLUMN + 1):
            column.append(xy_datas[:, i])
        print(column)



    def __find_mahalanobis_near(self, near_cities):
        xy_datas_vectors = [near_cities["X"],near_cities["Y"]]
        xy_datas = np.mat(xy_datas_vectors)

        dim = xy_datas.shape[0]  # x, y (2のはず)
        datas = xy_datas.shape[1]  # データ数
        print("dim:", dim, "  COL:", datas)

        # xy_datas: numpyの2次元配列[][]
        # row:行,column:列,ave:平均,vcm:分散共分散行列
        ave = [0.0 for i in range(dim)]  # ROWの数、0で初期化

        # 平均値の計算
        for i in range(dim):
            # スライスという技法
            ave[i] = np.average(xy_datas[i][0:len(xy_datas[i])])

        # 分散共分散行列を求める
        vcm = np.zeros((dim, dim))
        diff_vector = np.zeros((dim))
        for data_id in range(datas):
            for dim in range(dim):
                diff_vector[dim] = xy_datas[dim, data_id] - ave[dim]
            diff_vector_T = diff_vector[:, np.newaxis]
            vcm += diff_vector * diff_vector_T

        vcm = vcm / datas

        if np.linalg.cond(vcm) < 1 / np.sys.float_info.epsilon:
            # 逆行列が存在する時
            ivcm = np.linalg.inv(vcm)
        else:
            # 逆行列が存在しないときは、ユークリッド距離の計算
            # https://stackoverflow.com/questions/13249108/efficient-pythonic-check-for-singular-matrix
            ivcm = np.eye(dim)

        # マハラノビス距離計算
        nearest_dist = 10000000
        nearest = None
        for city_data_row in near_cities.iterrows():
            city_data = city_data_row[1]
            tmp_nearest_dist = sci.mahalanobis([city_data["X"], city_data["Y"]], ave, ivcm)
            if tmp_nearest_dist < nearest_dist:
                nearest_dist = tmp_nearest_dist
                nearest = city_data

        if nearest is None:
            nearest = near_cities[0]

        return nearest

    def find_nearest_city(self, from_city):
        near_cities = self.__find_eucledean_near(from_city)
        if near_cities is None or len(near_cities.index) == 0:
            return None
        nearest_city = self.__find_mahalanobis_near(near_cities)

        # 同じ座標に重複していることも考慮
        near_x = value2coordinate(nearest_city["X"])
        near_y = value2coordinate(nearest_city["Y"])
        self.img[near_y, near_x] = self.img[near_y, near_x] - nearest_city["CityId"]

        return nearest_city
