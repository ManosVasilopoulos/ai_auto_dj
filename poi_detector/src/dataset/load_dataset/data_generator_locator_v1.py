import pandas as pd
import numpy as np
import os


class SkaterbotDataGenerator:
    train_counter = 0
    train_successful = 0
    test_counter = 0
    test_successful = 0
    n_train = 0
    n_test = 0
    n_test_succesful = 0
    n_samples = 0
    max_seconds = 100
    max_time_steps = 0

    def __calculate_timesteps(self, time_size, window_size):
        time_steps = int(self.max_seconds * (1000 / window_size) / time_size)
        return time_steps

    def __init__(self, dataset_dir: str, csv_name: str,
                 time_size: int,
                 freq_size: int,
                 window_size: float,
                 transform_type: str,
                 train_test_ratio=0.7,
                 ):
        self.__check_train_test_ratio(train_test_ratio)
        self.transform_type = self.__check_transform(transform_type, window_size)

        self.dataset_dir = dataset_dir
        self.data_dir = os.path.join(dataset_dir, 'data')

        self.dataset = self.csv_to_data_list(os.path.join(dataset_dir, csv_name))

        self.time_size, self.freq_size, self.window_size = time_size, freq_size, window_size
        self.max_time_steps = self.__calculate_timesteps(time_size, window_size)

        self.train_set, self.test_set = self.__get_train_test_samples(train_test_ratio)

    def __check_transform(self, transform_type, window_size):
        if (transform_type == 'constant-q' or transform_type == 'cqt') and (window_size == 10 or window_size == 100):
            raise Exception(
                'SkaterbotDataGeneratorError: Cannot have Constant-Q transform with window-size==' + str(window_size))
        return transform_type

    def __check_train_test_ratio(self, ttr: float):
        if ttr > 1:
            raise Exception('SkaterbotDataGeneratorError: "train_test_ratio" should have a value lower than 1.')
        if ttr <= 0:
            raise Exception('SkaterbotDataGeneratorError: "train_test_ratio" should have a positive value.')

    @staticmethod
    def csv_to_data_list(csv_path: str):
        df = pd.read_csv(csv_path)
        return df.to_numpy()[:, 1]

    def extract_samplename_and_offset(self, offset_filename):
        offset_idx = offset_filename.find('_offset_')

        sample_name = offset_filename[:offset_idx]

        offset_path = os.path.join(self.data_dir, sample_name, 'offsets', 'time_size_' + str(self.time_size),
                                   offset_filename)
        start_idx, end_idx = np.load(offset_path)

        return sample_name, start_idx, end_idx

    def read_input(self, sample_name: str, start_idx: int, end_idx: int):
        sample_path = os.path.join(self.data_dir,
                                   sample_name,
                                   'inputs',
                                   sample_name + self.transform_type + '.npy')
        full_transform = np.load(sample_path)
        if start_idx + self.max_time_steps * self.time_size != end_idx:
            raise Exception('SkaterbotDataGeneratorError: the "time_size" given does not match'
                            'with the corresponding of the dataset. "time_size"s value should be equal '
                            'to ' + str(end_idx - start_idx) + '.')
        x = self.normalize_input(full_transform[start_idx: end_idx, :])
        if x.shape[0] < self.max_time_steps * self.time_size:
            return np.array([])
        x = np.reshape(x, (self.max_time_steps, self.time_size, self.freq_size))
        return x

    def read_output(self, sample_name: str, start_idx, end_idx: int):
        """
        :param sample_name: song_name (wav filename)
        :param start_idx: the sub-transform's starting point
        :param end_idx: the sub-transform's ending point
        :return: returns output batch
        """
        sample_path = os.path.join(self.data_dir, sample_name)
        sample_path = os.path.join(sample_path, 'output_raw', sample_name + '.npy')
        pois = np.load(sample_path)

        at_least_one_poi = False
        y = np.zeros(self.max_time_steps)

        for poi in pois:

            start_time = start_idx / (1000 / self.window_size)
            end_time = end_idx / (1000 / self.window_size)
            # If no pois correspond to the current input then the sample should be skipped
            if start_time <= poi < end_time:
                """ poi - start_time so that output sample is withing the range of "time_size / (1000 / ws)"  """
                poi_idx = int((poi * (1000 / self.window_size)) // self.max_time_steps)
                start_time_idx = int(start_idx // self.max_time_steps)
                if poi_idx - start_time_idx >= self.max_time_steps:
                    break
                y[poi_idx - start_time_idx] = 1
                at_least_one_poi = True
        if not at_least_one_poi:
            return np.array([])
        else:
            return y

    def normalize_input(self, x: np.ndarray):
        # Since spectrograms are converted to skimages of type uint8, the max value is 255 and the min 0
        max_val = np.amax(x)
        min_val = np.amin(x)
        if max_val > 255 or min_val < 0 or min_val == max_val:
            return np.array([])

        normalized_input = (x - min_val) / (max_val - min_val)

        return normalized_input

    def __initialize_train_set(self):
        self.train_counter = 0
        np.random.shuffle(self.train_set)

    def __initialize_test_set(self):
        self.test_counter = 0

    def __check_x(self, x):
        x_is_not_ok = False
        if x.size == 0:
            x_is_not_ok = True
        return x_is_not_ok

    def __check_y(self, y):
        y_is_not_ok = False
        if y.size < self.max_time_steps:
            y_is_not_ok = True
        return y_is_not_ok

    def __get_train_test_samples(self, ratio: float):
        self.n_samples = self.dataset.shape[0]
        self.n_train = int(self.n_samples * ratio)
        self.n_test = self.n_samples - self.n_train
        return self.dataset[:self.n_train], self.dataset[self.n_train:]

    def train_flow_locator_v1(self, batch_size: int):
        """
        :param batch_size: number of samples to be returned
        :return: x_train, y_train, numpy arrays in proper shapes for CNNs.
        """
        self.__initialize_train_set()

        while self.train_counter + batch_size < self.n_train:
            x_train, y_train = self.__make_train_batch_locator_v1(batch_size)
            yield x_train, y_train

        rest_of_data = self.n_train - self.train_counter
        if 0 < rest_of_data < batch_size:
            x_train, y_train = self.__make_train_batch_locator_v1(rest_of_data)

            yield x_train, y_train
        else:
            raise StopIteration

    def test_flow_locator_v1(self, batch_size: int):

        self.test_counter = 0

        while self.test_counter + batch_size < self.n_test:
            x_test, y_test = self.__make_test_batch_locator_v1(batch_size)
            yield x_test, y_test

        rest_of_data = self.n_test - self.test_counter
        if 0 < rest_of_data < batch_size:
            x_test, y_test = self.__make_test_batch_locator_v1(rest_of_data)
            yield x_test, y_test
        else:
            raise StopIteration

    def __make_train_batch_locator_v1(self, batch_size: int):
        x_train, y_train = self.__get_empty_batches_locator_v1()

        i = 0
        while i < batch_size:
            if self.train_counter == self.n_train:
                return np.array([]), np.array([])

            sample_name, start_idx, _ = self.extract_samplename_and_offset(
                self.train_set[self.train_counter])
            self.train_counter += 1

            end_idx = start_idx + self.time_size * self.max_time_steps

            x = self.read_input(sample_name, start_idx, end_idx)

            y = self.read_output(sample_name, start_idx, end_idx)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y)
            if x_is_not_ok or y_is_not_ok:
                continue
            x_train, y_train = self.__append_sample_locator_v1(x_train, y_train, x, y)
            i += 1

        return x_train, y_train

    def __make_test_batch_locator_v1(self, batch_size: int):
        x_test, y_test = self.__get_empty_batches_locator_v1()

        i = 0
        while i < batch_size:
            if self.test_counter == self.n_test:
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.test_set[self.test_counter])
            self.test_counter += 1

            end_idx = start_idx + self.time_size * self.max_time_steps

            x = self.read_input(sample_name, start_idx, end_idx)
            y = self.read_output(sample_name, start_idx, end_idx)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_test, y_test = self.__append_sample_locator_v1(x_test, y_test, x, y)
            i += 1
        return x_test, y_test

    def __get_empty_batches_locator_v1(self):
        x_train = np.empty((0, self.max_time_steps, self.time_size, self.freq_size))
        y_train = np.empty((0, self.max_time_steps))
        return x_train, y_train

    def __append_sample_locator_v1(self, x_batch, y_batch, x, y):
        if x.shape != (self.max_time_steps, self.time_size, self.freq_size):
            print('SkaterbotDataGenerator: Something went wrong with the current sample. Skipping it...')
            return x_batch, y_batch

        # A sample's shape is 3-dimensional. Thus we add one more dimension to make it image-like. (one colour)
        x_batch = np.append(x_batch, np.expand_dims(x, axis=0), axis=0)
        y_batch = np.append(y_batch, np.expand_dims(y, axis=0), axis=0)
        return x_batch, y_batch
