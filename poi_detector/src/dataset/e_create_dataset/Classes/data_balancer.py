import numpy as np
from random import randint
from os.path import join as os_path_join
from os import mkdir as os_mkdir


class DatasetBalancer:
    time_size = 0

    def set_time_size(self, time_size):
        self.time_size = time_size

    @staticmethod
    def get_initial_offset():
        return randint(0, 100)

    def make_offset_dir(self, save_dir):
        offsets_dir = os_path_join(save_dir, 'offsets')
        try:
            os_mkdir(offsets_dir)
        except FileExistsError:
            pass

        new_dir = os_path_join(offsets_dir, 'time_size_' + str(self.time_size))
        try:
            os_mkdir(new_dir)
        except FileExistsError:
            pass
        return new_dir + '/'

    @staticmethod
    def make_song_dir(dataset_dir, filename):
        new_dir = os_path_join(dataset_dir, filename)
        extentions = ['', 'inputs', 'output', ' output_raw', 'output_distribution', 'offsets']
        for extention in extentions:
            try:
                os_mkdir(os_path_join(new_dir, extention))
            except FileExistsError:
                pass
        return new_dir + '/'

    @staticmethod
    def __save_npy_array(save_dir, sample_name, arr):
        try:
            os_mkdir(save_dir)
        except FileExistsError:
            pass
        np.save(os_path_join(save_dir, sample_name + '.npy'), arr)

    def create_and_save_offsets(self, offset_dir, filename, time_freq_input, pois_output,
                                initial_offset, offset_step):
        offset = initial_offset
        while 1:
            subspec = time_freq_input[offset: offset + self.time_size]
            subpois = pois_output[offset: offset + self.time_size]
            if subspec.shape[0] < self.time_size or subpois.shape[0] < self.time_size:
                break
            self.save_offset(offset_dir, filename, offset)
            offset += offset_step

    def create_data(self, transform_input: np.ndarray, pois_vector: np.ndarray,
                    pois_list: np.ndarray,
                    dataset_dir: str,
                    filename: str,
                    transform_type: str,
                    offset_step: int,
                    write_output=True):

        new_dir = self.make_song_dir(dataset_dir, filename)

        self.save_input(new_dir, filename + transform_type, transform_input)
        if write_output:
            self.save_output(new_dir, filename, pois_vector, pois_list)

        self.create_output_offsets(new_dir, filename, transform_input, pois_vector, offset_step)

    def create_output_offsets(self, sample_dir, filename, time_freq_input, pois_output, offset_step):
        offset_dir = self.make_offset_dir(sample_dir)
        initial_offset = self.get_initial_offset()
        self.create_and_save_offsets(offset_dir, filename, time_freq_input, pois_output, initial_offset, offset_step)

    def save_offset(self, offset_dir: str, filename: str, offset: int):
        offset_name = '_offset_' + str(offset) + '.npy'
        offset_path = os_path_join(offset_dir, filename + offset_name)
        np.save(offset_path, np.array([offset, offset + self.time_size]))

    def get_samples_pois_counts(self, pois_output: np.ndarray, offset_stp: int):
        offset = self.get_initial_offset()
        counter_out = np.zeros(self.time_size)
        while 1:
            try:
                counter_out += pois_output[offset: offset + self.time_size]
                offset += offset_stp
                pass
            except:
                break
        return counter_out

    def save_input_output_pair(self, save_dir, sample_name,
                               transform: np.ndarray,
                               out: np.ndarray,
                               pois_list: np.ndarray):

        self.__save_npy_array(os_path_join(save_dir, 'inputs'), sample_name, transform)
        self.__save_npy_array(os_path_join(save_dir, 'output'), sample_name, out)
        self.__save_npy_array(os_path_join(save_dir, 'output_raw'), sample_name, pois_list)

    def save_input(self, save_dir, sample_name, transform):
        self.__save_npy_array(os_path_join(save_dir, 'inputs'), sample_name, transform)

    # NEEDS TO CHANGE - extention of dir should be argument along with its corresponding out-array
    # remove pois_list
    def save_output(self, save_dir, sample_name, out, pois_list):
        self.__save_npy_array(os_path_join(save_dir, 'output'), sample_name, out)
        self.__save_npy_array(os_path_join(save_dir, 'output_raw'), sample_name, pois_list)

    def save_output_distribution(self, save_dir, sample_name, out):
        self.__save_npy_array(os_path_join(save_dir, 'output_distribution'), sample_name, out)

    def find_standard_frame(self, poi: float):
        return int(poi // self.time_size)

    def in_standard_frame_poi_location(self, poi: float):
        return poi % self.time_size
