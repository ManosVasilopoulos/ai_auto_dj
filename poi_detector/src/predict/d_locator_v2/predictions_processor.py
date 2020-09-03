from numpy import ndarray as np_ndarray
from scipy.signal import find_peaks as scipy_find_peaks


class PredictionsProcessor:
    cue_point_limit = 50  # represents 10 seconds from start of song

    def find_peaks(self, vector: np_ndarray, height=0.05, distance=50):
        while 1:
            peaks_indexes, peaks_heights = scipy_find_peaks(vector, height=height, distance=distance)
            if peaks_indexes.shape[0] > 4:
                print('Found more than 4 peaks -->', peaks_indexes)
                height += 0.0001
            elif peaks_indexes.shape[0] < 4:
                if peaks_indexes.shape[0] == 3 and peaks_indexes[0] >= 100:
                    cue = self.find_cue_peak(vector)
                    return [cue, peaks_indexes[0], peaks_indexes[1], peaks_indexes[2]]
                print('Found less than 4 peaks -->', peaks_indexes)
                height -= 0.0001
            else:
                if peaks_indexes[0] > self.cue_point_limit:
                    cue = self.find_cue_peak(vector)
                    return [cue, peaks_indexes[0], peaks_indexes[1], peaks_indexes[2]]
                else:
                    return peaks_indexes

    def find_cue_peak(self, vector: np_ndarray):
        peak_index, _ = scipy_find_peaks(vector[0:self.cue_point_limit], distance=self.cue_point_limit)
        return peak_index[0]
