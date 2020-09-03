from basic_classes.data_balancer import Balancer
import numpy as np


class LocatorBalancer2(Balancer):

    def filter_inputs_outputs(self, time_freq_input: np.ndarray, pois_output: np.ndarray):
        final_ins = np.empty((0, self.time_size, self.freq_size))
        final_outs = np.empty((0, self.time_size))


        return final_ins, final_outs

    def find_standard_frame(self, poi: float):
        return int(poi // self.time_size)

    def in_standard_frame_poi_location(self, poi: float):
        return poi % self.time_size
