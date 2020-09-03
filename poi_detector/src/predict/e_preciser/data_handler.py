from os.path import join as os_path_join
from numpy import ndarray as np_ndarray
from numpy import array as np_array
from numpy import reshape as np_reshape
from skimage.io import imread

class PreciserDataHandler:
    n_samples = 0
    max_seconds = 100
    min_val = 0
    max_val = 255

    def __check_transform(self, transform_type, window_size):
        if (transform_type == 'constant-q' or transform_type == 'cqt') and (window_size == 10 or window_size == 100):
            raise Exception(
                'SkaterbotDataGeneratorError: Cannot have Constant-Q transform with window-size==' + str(window_size))
        return transform_type

    def __check_indexes(self, start_idx: int, end_idx: int):
        if start_idx + self.time_size != end_idx:
            raise Exception('SkaterbotDataGeneratorError: the "time_size" given does not match'
                            'with the corresponding of the dataset. "time_size"s value should be equal '
                            'to ' + str(end_idx - start_idx) + '.')

    def __init__(self, data_dir: str,
                 time_size: int,
                 freq_size: int,
                 window_size: float,
                 transform_type: str,
                 ):
        self.transform_type = self.__check_transform(transform_type, window_size)

        self.data_dir = data_dir

        self.time_size, self.freq_size, self.window_size = time_size, freq_size, window_size

    def read_full_transform(self, sample_name):
        return imread(os_path_join(self.data_dir, sample_name))

    def read_input(self, sample_name: str, start_idx: int, end_idx: int):

        self.__check_indexes(start_idx, end_idx)

        full_transform = self.read_full_transform(sample_name)
        if full_transform.shape[0] < self.time_size:
            return np_array([])

        x = self.normalize_input(full_transform[start_idx: end_idx, :])
        return np_reshape(x, (1, self.time_size, self.freq_size, 1))

    def normalize_input(self, x: np_ndarray):
        # Since spectrograms are converted to skimages of type uint8, the max value is 255 and the min 0
        return (x - self.min_val) / (self.max_val - self.min_val)
