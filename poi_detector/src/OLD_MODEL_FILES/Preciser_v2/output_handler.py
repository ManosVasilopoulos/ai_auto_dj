import numpy as np
from basic_classes.output_handler import OutputHandler
from basic_classes.constants import MAX_SAMPLES


class OutputPreciserHandler(OutputHandler):

    def get_output(self, poi_list, unique_outs=False):
        out, idxs = self.__output_preciser(poi_list)
        return out, idxs

    def __output_preciser(self, row, unique_outs=False):
        seconds = self.time_size / (1000 // self.window_size)
        idxs = []

        """ Keep two decimals """
        out = np.empty((0, 1))
        for u in row:
            if u < 0:
                continue
            if u >= MAX_SAMPLES / (1000 // self.window_size):
                break
            idx = int(u // seconds)
            label_index = int((u % seconds) * (1000 // self.window_size) - 1)
            if unique_outs and len(idxs) > 0:
                if idx == idxs[len(idxs) - 1]:
                    # print('..............Same Indexes Detected..............')
                    continue
            label_index = np.expand_dims(np.array([label_index]), axis=0)
            out = np.append(out, label_index, axis=0)
            idxs.append(idx)
        return np.array(out), idxs

