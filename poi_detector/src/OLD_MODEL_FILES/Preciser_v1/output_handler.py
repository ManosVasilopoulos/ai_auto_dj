import numpy as np
from basic_classes.output_handler import OutputHandler
from basic_classes.constants import MAX_SAMPLES


class OutputPreciserHandler(OutputHandler):

    def get_output(self, poi_list, unique_outs=False):
        out = self.__output_preciser(poi_list)
        return out

    def __output_preciser(self, row, unique_outs=False):
        seconds = self.time_size / (1000 // self.window_size)
        out = []
        idxs = []

        """ Keep two decimals """
        for u in row:
            if u < 0:
                continue
            if u >= MAX_SAMPLES / (1000 // self.window_size):
                break
            """ TEMPORARY"""
            idx = int(u // seconds)
            t_in_frame = (u % seconds) / seconds
            if unique_outs and len(idxs) > 0:
                if idx == idxs[len(idxs) - 1]:
                    # print('..............Same Indexes Detected..............')
                    continue
            out.append(t_in_frame)
            idxs.append(idx)
        return np.array(out), idxs


