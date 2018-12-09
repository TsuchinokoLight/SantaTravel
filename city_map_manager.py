import pandas as pd
import numpy as np

from city_explorer import CityExplorer
from util import value2coordinate

class CityMapManager:
    def __init__(self, csv_name="cities.csv"):
        self.rest_city_df = pd.read_csv(csv_name)
        self.here = self.__pop_city(0)
        self.img = self.__make_citymap_image()

    def __pop_city(self, target_city_id):
        city_ids = self.rest_city_df["CityId"].iloc
        for index in range(self.rest_city_df.shape[0]):
            if target_city_id == city_ids[index]:
                self.rest_city_df, next_city = self.rest_city_df.drop(index), self.rest_city_df.loc[index]
                self.rest_city_df.reset_index(drop=True, inplace=True)
                return next_city

        return None

    def pop_next_city(self):
        city_explorer = CityExplorer(self.img, self.rest_city_df)
        near_cities = city_explorer.find_eucledean_near(self.here)
        if len(near_cities) == 0 or near_cities is None:
            return None
        self.rest_city_df = city_explorer.rest_city_df
        self.img = city_explorer.img

        # 本来はここでfind_mahalanobis_near使う
        # とりあえず先頭返す
        near_city = near_cities[0]
        # roundしたため、同じ座標に重複していることも考慮
        near_x = value2coordinate(near_city["X"])
        near_y = value2coordinate(near_city["Y"])
        self.img[near_y, near_x] = self.img[near_y, near_x] - near_city["CityId"]

        return self.__pop_city(near_city["CityId"])


    def __make_citymap_image(self):
        rows = int(round(self.rest_city_df["Y"].max()))+1  # roundは苦渋の選択・・・
        cols = int(round(self.rest_city_df["X"].max()))+1
        img = np.zeros((rows, cols), dtype=np.uint8)

        # 画素値に街番号入れる処理
        x_arr = self.rest_city_df["X"].values
        y_arr = self.rest_city_df["Y"].values
        id_arr = self.rest_city_df["CityId"].values
        for index in range(self.rest_city_df.shape[0]):
            x = value2coordinate(x_arr[index])
            y = value2coordinate(y_arr[index])
            img[y, x] = id_arr[index]
        return img
