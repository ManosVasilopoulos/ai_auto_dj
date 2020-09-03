import numpy as np
from abc import ABC, abstractmethod


class OutputHandler(ABC):
    song_length = 0
    time_size = 0

    def __init__(self, window_size: float):
        self.window_size = window_size

    def set_time_size(self, time_size):
        self.time_size = time_size

    @abstractmethod
    def get_output(self, poi_list: list):
        return

    @staticmethod
    def keep_two_decimals(pois_list: list):
        new_row = np.array([u * 100 for u in pois_list])
        mapper = np.vectorize(round)
        new_row = mapper(new_row) / 100
        return new_row

    def pois_to_full_one_hot(self, pois_list: list, song_duration: int):
        one_hot = np.zeros(song_duration)
        for poi in pois_list:
            idx = int(poi * (1000/self.window_size))
            one_hot[idx] = 1.0
        return one_hot
