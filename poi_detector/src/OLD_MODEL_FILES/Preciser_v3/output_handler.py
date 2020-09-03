import numpy as np
from basic_classes.output_handler import OutputHandler
from basic_classes.constants import MAX_SAMPLES


class OutputPreciserHandler(OutputHandler):
    song_length = 0

    def set_song_length(self, song_length):
        self.song_length = song_length

    def get_output(self, poi_list, extras=False):
        out = self.__output_preciser(poi_list)
        final_out = self.__get_shaped_output(out, extras)

        return final_out

    def __output_preciser(self, row):
        """
        :param row: list of Points of Interest (float)
        :return: numpy array as long as the spectrogram it corresponds to. Each poi is marked with 1s.
        The rest of its values are 0s.
        """
        out = np.zeros(self.song_length)
        """ Keep two decimals """
        for u in row:
            if u < 0:
                continue
            poi_idx = int(u * (1000 / self.window_size))
            out[poi_idx] = 1.0
        return out

    def list_to_vector(self, poi_list):
        out = np.zeros(self.song_length)
        for poi in poi_list:
            poi_idx = int(poi * (1000 // self.window_size))
            out[poi_idx] = 1.0
        return out

    def __get_shaped_output(self, out, extras=False):
        """
        :param out: numpy array returned from "__output_preciser"
        :param extras: if this value is True, extra P.O.I. are added.
        :return: numpy array with stacked numpy 'vectors' of 0s and 1s. Each 'vector' has the same length
        as the length of a subspectrogram that is used as input to a CNN.
        """
        final_out = np.empty((0, self.time_size))

        first_out = out[:self.time_size]
        final_out = np.append(final_out, first_out)

        if extras:
            step = 101
            i = 100
        else:
            step = self.time_size
            i = self.time_size

        while i < self.song_length - step:
            mid_out = out[i: i + self.time_size]
            final_out = np.append(final_out, mid_out)
            i += step

        last_out = out[-self.time_size:]
        final_out = np.append(final_out, last_out)

        return final_out
