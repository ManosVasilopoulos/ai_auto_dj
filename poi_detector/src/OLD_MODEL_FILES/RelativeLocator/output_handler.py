import numpy as np
from basic_classes.output_handler import OutputHandler
from basic_classes.constants import MAX_SAMPLES


class OutputLocatorHandler(OutputHandler):

    def get_output(self, poi_list, last_subspec_id=-1):
        if last_subspec_id < 0:
            raise Exception('OutputLocatorHandler: "last_subspec_id" cannot have a value lower than zero.')
        out = self.__output_locator(poi_list, last_subspec_id)
        return out

    def __output_locator(self, row, last_subspec_id):
        timesteps = int(MAX_SAMPLES // self.time_size)
        seconds = self.time_size / (1000 // self.window_size)
        out = np.zeros((timesteps, 1))
        out[last_subspec_id, 0] = 1.0
        for u in row:
            if u >= MAX_SAMPLES / (1000 // self.window_size):
                break
            idx = int(u // seconds)
            out[idx, 0] = 1.0
        return out

