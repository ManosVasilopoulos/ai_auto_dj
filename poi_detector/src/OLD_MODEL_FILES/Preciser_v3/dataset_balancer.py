import numpy as np
from basic_classes.data_balancer import Balancer


class PreciserBalancer(Balancer):

    def filter_inputs_outputs(self, time_freq_input: np.ndarray, pois_output: np.ndarray):
        final_ins = np.empty((0, self.time_size, self.freq_size))
        final_outs = np.empty((0, self.time_size))

        for poi in pois_output:
            i = self.find_standard_frame(poi)

            d = int(self.in_standard_frame_poi_location(poi) * (1000 // self.window_size))

            mi = max(d, self.time_size - d)

            if mi == d:
                offsets = [-90, -65, -40, -15, 0]
            else:
                offsets = [0, 15, 40, 65, 90]

            for offset in offsets:
                try:
                    start_idx = i * self.time_size + offset
                    end_idx = (i + 1) * self.time_size + offset
                    in_subspec = time_freq_input[start_idx: end_idx]

                    out_poi = np.zeros(self.time_size)
                    out_poi[d + offset] = 1.0

                    final_ins = np.append(final_ins, np.expand_dims(in_subspec, axis=0))
                    final_outs = np.append(final_outs, np.expand_dims(out_poi, axis=0))
                except:
                    continue

        return final_ins, final_outs

    def find_standard_frame(self, poi: float):
        return int(poi // self.time_size)

    def in_standard_frame_poi_location(self, poi: float):
        return poi % self.time_size
