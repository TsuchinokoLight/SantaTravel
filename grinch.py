# -*- coding: utf-8 -*-
import city_map_manager
from util import calc_distance


class Grinch:
    def __init__(self, city_map=city_map_manager.CityMapManager()):
        self.city_map = city_map
        self.meter = 0
        self.record = ["Path"]
        self.keep_record(self.city_map.here)

    def output_record(self):
        # CSVへ書き込み
        record_str = '\n'.join(self.record)
        with open("submission.csv", 'wt') as f:
            f.write(record_str)

    def keep_record(self, city):
        self.record.append(str(int(city["CityId"])))

    def goto(self, next_city):
        here = self.city_map.here
        self.meter += calc_distance(here["X"], here["Y"], next_city["X"], next_city["Y"])
        self.city_map.here = next_city

    def start_hell_odyssey(self):
        while True:
            # データ群から一つ取り出し（ポップ）して、移動
            try:
                next_city = self.city_map.pop_next_city()
                if next_city is None:
                    print("END")
                    self.output_record()
                    return
            except StopIteration:
                return

            # ポイントへ移動
            self.goto(next_city)

            # 記録
            self.keep_record(next_city)

