from poi_detector.src.basic_classes.output_handler import OutputHandler
import numpy as np


class OutputDatasetHandler(OutputHandler):

    def get_output(self, poi_list: list):
        raise Exception('OutputLocatorHandler2 Error: "get_output" has not been implemented.')

    def list_to_vector(self, poi_list: list, transform_length: int):
        out = np.zeros(transform_length)
        for poi in poi_list:
            poi_idx = int(poi * (1000 // self.window_size))
            out[poi_idx] = 1.0
        return out

    def list_to_distribution_vector(self, poi_list: list, transform_length: int):
        out = np.zeros(transform_length)
        for poi in poi_list:
            poi_idx = int(poi * (1000 // self.window_size))
            for j in range(-5, 6):
                if 0 <= poi_idx + j < out.size:
                    out[poi_idx + j] = 1.0 / (1.0 + abs(j))
        return out
