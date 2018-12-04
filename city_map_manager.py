import pandas as pd
import matplotlib.pyplot as plt

from util import calc_distance


class CityMapManager:
    def __init__(self, csv_name="cities.csv"):
        self.rest_city_df = pd.read_csv(csv_name)
        self.here = self.__pop_city(0)

    def print_graph(self):
        #plt.scatter(self.city_map[['X']], self.city_map[['Y']], s=0.1)
        plt.show()

    def __pop_city(self, index):
        self.rest_city_df, next_city = self.rest_city_df.drop(index), self.rest_city_df.loc[index]
        return next_city

    def pop_next_city(self):
        index = self.__find_euclidean_near(center=self.here)
        return self.__pop_city(index)

    def find_mahalanobis_near(self, from_here):
        # return city index
        return 0

    def __find_euclidean_near(self, center):
        min_distance = 384400000  # Lunar distance
        dest_city_index = None
        for index, proposed_dest in self.rest_city_df.iterrows():
            proposed_dest_distance = calc_distance(from_city=center, dest_city=proposed_dest)
            if proposed_dest_distance < min_distance:
                min_distance = proposed_dest_distance
                dest_city_index = index

        if dest_city_index is None:
            print("NO CITY Error")
            raise StopIteration

        return dest_city_index
