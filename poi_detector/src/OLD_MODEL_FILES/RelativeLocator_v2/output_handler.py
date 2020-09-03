from basic_classes.output_handler import OutputHandler
import numpy as np


class OutputLocatorHandler2(OutputHandler):

    def get_output(self, poi_list: list):
        raise Exception('OutputLocatorHandler2 Error: "get_output" has not been implemented.')

    def list_to_vector(self, poi_list: list):
        out = np.zeros(self.song_length)
        for poi in poi_list:
            poi_idx = int(poi * (1000 // self.window_size))
            out[poi_idx] = 1.0
        return out
