import pandas as pd
import matplotlib.pyplot as plt


class CityMapManager:
    def __init__(self, csv_name="cities.csv"):
        self.city_df = pd.read_csv(csv_name)
        self.citys_gen = self.__get_next_city_gen()

    def print_graph(self):
        plt.scatter(self.city_map[['X']], self.city_map[['Y']], s=0.1)
        plt.show()

    def __get_next_city_gen(self):
        for index, row in self.city_df.iterrows():
            yield row

    def pop_next_city(self):
        # self.citys, next_city = self.citys.drop(self.citys.head(1).index), self.citys.head(1)
        return self.citys_gen.__next__()
