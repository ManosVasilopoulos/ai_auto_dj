import pandas as pd
import numpy as np
import os


class SkaterbotDataGenerator:
    train_counter = 0
    train_successful = 0
    validation_counter = 0
    validation_succesful = 0
    test_counter = 0
    test_successful = 0
    n_train = 0
    n_validation = 0
    n_test = 0
    n_test_succesful = 0
    n_samples = 0
    max_time_steps = 100

    def __init__(self, dataset_dir: str, csv_name: str,
                 time_size: int,
                 freq_size: int,
                 window_size: float,
                 transform_type: str,
                 train_test_ratio=0.7,
                 validation_ratio=0.2):
        self.__check_ratio(train_test_ratio)
        self.__check_ratio(validation_ratio)
        self.transform_type = self.__check_transform(transform_type, window_size)

        self.dataset_dir = dataset_dir
        self.data_dir = os.path.join(dataset_dir, 'data')

        self.dataset = self.csv_to_data_list(os.path.join(dataset_dir, csv_name))

        self.time_size, self.freq_size, self.window_size = time_size, freq_size, window_size

        self.train_set, self.validation_set, self.test_set = self.__get_train_test_samples(train_test_ratio,
                                                                                           validation_ratio)

    # Main methods to be used.
    def train_flow(self, batch_size: int, regression_mode=False):
        """
        :param batch_size: number of samples to be returned
        :param regression_mode: default value False, if True the output samples are float and in_frame.
        :return: x_train, y_train, numpy arrays in proper shapes for CNNs.
        """
        self.__initialize_train_set()

        while self.train_counter + batch_size < self.n_train:
            x_train, y_train = self.__make_train_batch(batch_size, regression_mode)
            yield x_train, y_train

        rest_of_data = self.n_train - self.train_counter
        if 0 < rest_of_data < batch_size:
            x_train, y_train = self.__make_train_batch(rest_of_data, regression_mode)

            yield x_train, y_train
        else:
            raise StopIteration

    def validation_flow(self, batch_size: int, regression_mode=False):
        """
                :param batch_size: number of samples to be returned
                :param regression_mode: default value False, if True the output samples are float and in_frame.
                :return: x_train, y_train, numpy arrays in proper shapes for CNNs.
                """
        self.__initialize_validation_set()

        while self.validation_counter + batch_size < self.n_validation:
            x_validation, y_validation = self.__make_validation_batch(batch_size, regression_mode)
            yield x_validation, y_validation

        rest_of_data = self.n_validation - self.validation_counter
        if 0 < rest_of_data < batch_size:
            x_validation, y_validation = self.__make_validation_batch(rest_of_data, regression_mode)

            yield x_validation, y_validation
        else:
            raise StopIteration

    def test_flow(self, batch_size: int, regression_mode=False):

        self.test_counter = 0

        while self.test_counter + batch_size < self.n_test:
            x_test, y_test = self.__make_test_batch(batch_size, regression_mode)
            yield x_test, y_test

        rest_of_data = self.n_test - self.test_counter
        if 0 < rest_of_data < batch_size:
            x_test, y_test = self.__make_test_batch(rest_of_data, regression_mode)
            yield x_test, y_test
        else:
            raise StopIteration

    def train_flow2(self, batch_size: int, regression_mode=False):
        """
        :param batch_size: number of samples to be returned
        :param regression_mode: default value False, if True the output samples are float and in_frame.
        :return: x_train, y_train, numpy arrays in proper shapes for CNNs.
        """
        self.__initialize_train_set()

        while self.train_counter + batch_size < self.n_train:
            x_train, y_train = self.__make_train_batch2(batch_size, regression_mode)
            yield x_train, y_train

        rest_of_data = self.n_train - self.train_counter
        if 0 < rest_of_data < batch_size:
            x_train, y_train = self.__make_train_batch2(rest_of_data, regression_mode)

            yield x_train, y_train
        else:
            raise StopIteration

    def validation_flow2(self, batch_size: int, regression_mode=False):
        """
                :param batch_size: number of samples to be returned
                :param regression_mode: default value False, if True the output samples are float and in_frame.
                :return: x_train, y_train, numpy arrays in proper shapes for CNNs.
                """
        self.__initialize_validation_set()

        while self.validation_counter + batch_size < self.n_validation:
            x_validation, y_validation = self.__make_validation_batch2(batch_size, regression_mode)
            yield x_validation, y_validation

        rest_of_data = self.n_validation - self.validation_counter
        if 0 < rest_of_data < batch_size:
            x_validation, y_validation = self.__make_validation_batch2(rest_of_data, regression_mode)

            yield x_validation, y_validation
        else:
            raise StopIteration

    def test_flow2(self, batch_size: int, regression_mode=False):

        self.test_counter = 0

        while self.test_counter + batch_size < self.n_test:
            x_test, y_test = self.__make_test_batch2(batch_size, regression_mode)
            yield x_test, y_test

        rest_of_data = self.n_test - self.test_counter
        if 0 < rest_of_data < batch_size:
            x_test, y_test = self.__make_test_batch2(rest_of_data, regression_mode)
            yield x_test, y_test
        else:
            raise StopIteration

    def input_flow(self, batch_size: int):
        """
        :param batch_size: number of samples to be returned
        :param regression_mode: default value False, if True the output samples are float and in_frame.
        :return: x_train, y_train, numpy arrays in proper shapes for CNNs.
        """
        self.__initialize_input_set()

        while self.train_counter + batch_size <= self.n_train:
            x_train = self.__make_input_batch(batch_size)
            yield x_train

        rest_of_data = self.n_train - self.train_counter
        if 0 < rest_of_data < batch_size:
            x_train = self.__make_input_batch(batch_size)
            yield x_train
        else:
            raise StopIteration

    """ Other methods """
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
        if start_idx + self.time_size != end_idx:
            raise Exception('SkaterbotDataGeneratorError: the "time_size" given does not match'
                            'with the corresponding of the dataset. "time_size"s value should be equal '
                            'to ' + str(end_idx - start_idx) + '.')
        x = self.normalize_input(full_transform[start_idx: end_idx, :])
        return x

    def read_output(self, sample_name: str, start_idx, end_idx: int, regression_mode=False):
        """
        :param sample_name: song_name (wav filename)
        :param start_idx: the sub-transform's starting point
        :param end_idx: the sub-transform's ending point
        :param regression_mode: Default value False, if True the output samples are float and in_frame.
        :return: returns output batch
        """
        sample_path = os.path.join(self.data_dir, sample_name)
        if regression_mode:
            sample_path = os.path.join(sample_path, 'output_raw', sample_name + '.npy')
            pois = np.load(sample_path)
            for poi in pois:

                start_time = start_idx / (1000 / self.window_size)
                end_time = end_idx / (1000 / self.window_size)
                # If no pois correspond to the current input then the sample should be skipped
                if start_time <= poi < end_time:
                    """ poi - start_time so that output sample is withing the range of "time_size / (1000 / ws)"  """
                    return np.array([poi - start_time])
        else:
            sample_path = os.path.join(sample_path, 'output', sample_name + '.npy')
            full_time_size_vector = np.load(sample_path)
            # If no pois correspond to the current input then the sample should be skipped
            if full_time_size_vector[start_idx: end_idx].any():
                return full_time_size_vector[start_idx: end_idx]

        # This way if no pois found in this frame we can use the empty array to skip this step
        return np.array([])

    # This method should not be implemented this way ==> Should be merged somehow with "read_output"
    def read_output_distribution(self, sample_name: str, start_idx, end_idx: int):
        """
        :param sample_name: song_name (wav filename)
        :param start_idx: the sub-transform's starting point
        :param end_idx: the sub-transform's ending point
        :param regression_mode: Default value False, if True the output samples are float and in_frame.
        :return: returns output batch
        """
        sample_path = os.path.join(self.data_dir, sample_name)
        sample_path = os.path.join(sample_path, 'output_distribution', sample_name + '.npy')
        full_time_size_vector = np.load(sample_path)
        # If no pois correspond to the current input then the sample should be skipped
        if full_time_size_vector[start_idx: end_idx].any():
            return full_time_size_vector[start_idx: end_idx]

        # This way if no pois found in this frame we can use the empty array to skip this step
        return np.array([])

    def normalize_input(self, x: np.ndarray):
        # Since spectrograms are converted to skimages of type uint8, the max value is 255 and the min 0
        max_val = np.amax(x)
        min_val = np.amin(x)
        if max_val > 255 or min_val < 0 or min_val == max_val:
            return np.array([])

        normalized_input = (x - min_val) / (max_val - min_val)

        return normalized_input

    # Private methods
    def __check_transform(self, transform_type, window_size):
        if (transform_type == 'constant-q' or transform_type == 'cqt') and (window_size == 10 or window_size == 100):
            raise Exception(
                'SkaterbotDataGeneratorError: Cannot have Constant-Q transform with window-size==' + str(window_size))
        return transform_type

    def __check_ratio(self, ttr: float):
        if ttr > 1:
            raise Exception('SkaterbotDataGeneratorError: "train_test_ratio" should have a value lower than 1.')
        if ttr <= 0:
            raise Exception('SkaterbotDataGeneratorError: "train_test_ratio" should have a positive value.')

    def __initialize_input_set(self):
        self.train_counter = 0

    def __make_input_batch(self, batch_size):
        x_batch = np.empty((0, self.time_size, self.freq_size, 1))

        i = 0
        while i < batch_size:
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.train_set[self.train_counter])
            self.train_counter += 1

            x = self.read_input(sample_name, start_idx, end_idx)

            x_is_not_ok = self.__check_x(x)
            if x_is_not_ok:
                continue

            x_batch = self.__append_input(x_batch, x)
            i += 1

        return x_batch

    def __append_input(self, x_batch, x):

        if len(x.shape) == 1:
            raise Exception(
                'SkaterbotDataGenerator: Something went wrong. The input "x" that was given had one dimension'
                'instead of 2 or more.')
        # A transform's shape is 2-dimensional. Thus we add one more dimension to make it image-like. (one colour)
        if len(x.shape) == 2:
            x = np.expand_dims(x, axis=-1)

        x_batch = np.append(x_batch, np.expand_dims(x, axis=0), axis=0)
        return x_batch

    def __initialize_train_set(self):
        self.train_counter = 0
        np.random.shuffle(self.train_set)

    def __initialize_validation_set(self):
        self.validation_counter = 0

    def __initialize_test_set(self):
        self.test_counter = 0

    def __get_empty_batches(self, regression_mode):
        x_train = np.empty((0, self.time_size, self.freq_size, 1))
        if regression_mode:
            y_train = np.empty((0, 1))
        else:
            y_train = np.empty((0, self.time_size))
        return x_train, y_train

    def __append_sample(self, x_batch, y_batch, x, y):
        if x.shape != (self.time_size, self.freq_size):
            print('Skipped this sample...')
            return x_batch, y_batch
        else:
            # A transform's shape is 2-dimensional. Thus we add one more dimension to make it image-like. (one colour)
            x = np.expand_dims(x, axis=-1)

        x_batch = np.append(x_batch, np.expand_dims(x, axis=0), axis=0)
        y_batch = np.append(y_batch, np.expand_dims(y, axis=0), axis=0)
        return x_batch, y_batch

    def __make_train_batch(self, batch_size: int, regression_mode: bool):
        x_train, y_train = self.__get_empty_batches(regression_mode)

        i = 0
        while i < batch_size:
            if self.train_counter == self.n_train:
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.train_set[self.train_counter])
            self.train_counter += 1
            x = self.read_input(sample_name, start_idx, end_idx)

            y = self.read_output(sample_name, start_idx, end_idx, regression_mode)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y, regression_mode)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_train, y_train = self.__append_sample(x_train, y_train, x, y)
            i += 1

        return x_train, y_train

    def __make_validation_batch(self, batch_size: int, regression_mode: bool):
        x_validation, y_validation = self.__get_empty_batches(regression_mode)

        i = 0
        while i < batch_size:
            if self.validation_counter == self.n_validation:
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.validation_set[self.validation_counter])
            self.validation_counter += 1
            x = self.read_input(sample_name, start_idx, end_idx)

            y = self.read_output(sample_name, start_idx, end_idx, regression_mode)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y, regression_mode)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_validation, y_validation = self.__append_sample(x_validation, y_validation, x, y)
            i += 1

        return x_validation, y_validation

    def __make_test_batch(self, batch_size: int, regression_mode: bool):
        x_test, y_test = self.__get_empty_batches(regression_mode)

        i = 0
        while i < batch_size:
            if self.test_counter == self.n_test:
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.test_set[self.test_counter])
            self.test_counter += 1

            x = self.read_input(sample_name, start_idx, end_idx)
            y = self.read_output(sample_name, start_idx, end_idx, regression_mode)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y, False)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_test, y_test = self.__append_sample(x_test, y_test, x, y)
            i += 1
        return x_test, y_test

    def __make_train_batch2(self, batch_size: int, regression_mode: bool):
        x_train, y_train = self.__get_empty_batches(regression_mode)

        i = 0
        while i < batch_size:
            if self.train_counter == self.n_train:  # Reached end of dataset
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.train_set[self.train_counter])
            self.train_counter += 1
            x = self.read_input(sample_name, start_idx, end_idx)

            y = self.read_output_distribution(sample_name, start_idx, end_idx)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y, regression_mode)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_train, y_train = self.__append_sample(x_train, y_train, x, y)
            i += 1

        return x_train, y_train

    def __make_validation_batch2(self, batch_size: int, regression_mode: bool):
        x_validation, y_validation = self.__get_empty_batches(regression_mode)

        i = 0
        while i < batch_size:
            if self.validation_counter == self.n_validation:
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.validation_set[self.validation_counter])
            self.validation_counter += 1
            x = self.read_input(sample_name, start_idx, end_idx)

            y = self.read_output_distribution(sample_name, start_idx, end_idx)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y, regression_mode)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_validation, y_validation = self.__append_sample(x_validation, y_validation, x, y)
            i += 1

        return x_validation, y_validation

    def __make_test_batch2(self, batch_size: int, regression_mode: bool):
        x_test, y_test = self.__get_empty_batches(regression_mode)

        i = 0
        while i < batch_size:
            if self.test_counter == self.n_test:  # Reached end of dataset
                return np.array([]), np.array([])
            sample_name, start_idx, end_idx = self.extract_samplename_and_offset(
                self.test_set[self.test_counter])
            self.test_counter += 1

            x = self.read_input(sample_name, start_idx, end_idx)
            y = self.read_output_distribution(sample_name, start_idx, end_idx)

            x_is_not_ok = self.__check_x(x)
            y_is_not_ok = self.__check_y(y, False)
            if x_is_not_ok or y_is_not_ok:
                continue

            x_test, y_test = self.__append_sample(x_test, y_test, x, y)
            i += 1
        return x_test, y_test

    def __check_x(self, x):
        x_is_not_ok = False
        if x.size == 0:
            x_is_not_ok = True
        return x_is_not_ok

    def __check_y(self, y, regression_mode):
        y_is_not_ok = False
        if y.size < self.time_size and not regression_mode:
            y_is_not_ok = True
        if y.size != 1 and regression_mode:
            y_is_not_ok = True
        return y_is_not_ok

    def __get_train_test_samples(self, train_test_ratio: float, validation_ratio: float):
        self.n_samples = self.dataset.shape[0]
        temp_n_train = int(self.n_samples * train_test_ratio)
        self.n_test = self.n_samples - self.n_train

        self.n_validation = int(temp_n_train * validation_ratio)
        self.n_train = temp_n_train - self.n_validation

        train_set = self.dataset[:self.n_train]
        validation_set = self.dataset[self.n_train: self.n_train + self.n_validation]
        test_set = self.dataset[self.n_train + self.n_validation:]

        return train_set, validation_set, test_set
