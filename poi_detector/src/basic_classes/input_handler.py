import librosa
from abc import ABC, abstractmethod
from . import constants
from .transforms import Transform
import numpy as np
import skimage.io
from .constants import temp_image_dir
import os


class InputHandler(ABC):
    song_length = 0
    freq_size = 0
    time_size = 0
    min_val = 0
    max_val = 255

    def __init__(self, transform_type: str, window_size: float):
        self.transform_type = transform_type
        self.window_size = window_size

        self.transformer = Transform()
        self.saved_transforms_directory = self.__get_saved_transforms_directory()

    def set_freq_size(self, freq_size):
        self.freq_size = freq_size

    def set_time_size(self, time_size):
        self.time_size = time_size

    def set_song_length(self, song_length):
        self.song_length = song_length

    def __get_min_val(self):
        if self.transform_type == 'spectrogram':
            return constants.MIN_VAL_SPEC
        elif self.transform_type == 'melspectrogram':
            return constants.MIN_VAL_MELSPEC
        elif self.transform_type == 'mfcc':
            return constants.MIN_VAL_MFCC
        elif self.transform_type == 'cqt':
            return constants.MIN_VAL_CQT
        else:
            raise Exception('InputHandler: Wrong transform type-->' + self.transform_type)

    def __get_max_val(self):
        if self.transform_type == 'spectrogram':
            return constants.MAX_VAL_SPEC
        elif self.transform_type == 'melspectrogram':
            return constants.MAX_VAL_MELSPEC
        elif self.transform_type == 'mfcc':
            return constants.MAX_VAL_MFCC
        elif self.transform_type == 'cqt':
            return constants.MAX_VAL_CQT
        else:
            raise Exception('InputHandler: Wrong transform type-->' + self.transform_type)

    def __get_saved_transforms_directory(self):
        base_dir = constants.base_transforms_dir
        if self.transform_type == 'spectrogram':
            return base_dir + 'Spectrograms/' + str(self.window_size) + '/' + str(self.freq_size) + '/'
        elif self.transform_type == 'melspectrogram':
            return base_dir + 'Melspectrograms/' + str(self.window_size) + '/' + str(self.freq_size) + '/'
        elif self.transform_type == 'mfcc':
            return base_dir + 'MFCCs/' + str(self.window_size) + '/' + str(self.freq_size) + '/'
        elif self.transform_type == 'cqt':
            return base_dir + 'Constant-Qs/' + str(self.freq_size) + '/'
        else:
            raise Exception('InputHandler: Wrong transform type-->' + self.transform_type)

    def __get_transform(self, samples: np.ndarray, sample_rate: int, transform_type=None, freq_size=None):
        if transform_type:
            if freq_size:
                transform = self.transformer.calculate_transform(samples,
                                                                 sample_rate,
                                                                 transform_type,
                                                                 freq_size,
                                                                 self.window_size)
            else:
                transform = self.transformer.calculate_transform(samples,
                                                                 sample_rate,
                                                                 transform_type,
                                                                 self.freq_size,
                                                                 self.window_size)
        else:
            if freq_size:
                transform = self.transformer.calculate_transform(samples,
                                                                 sample_rate,
                                                                 self.transform_type,
                                                                 freq_size,
                                                                 self.window_size)
            else:
                transform = self.transformer.calculate_transform(samples,
                                                                 sample_rate,
                                                                 self.transform_type,
                                                                 self.freq_size,
                                                                 self.window_size)
        return transform

    def read_audio(self, sample_name: str):
        samples, sample_rate = librosa.load(constants.wav_dir + sample_name, mono=True, sr=44100)
        return samples, sample_rate

    def calculate_input(self, sample_name: str, transform_type=None, freq_size=None):
        samples, sample_rate = librosa.load(constants.wav_dir + sample_name, mono=True, sr=44100)
        transform = self.__get_transform(samples, sample_rate, transform_type, freq_size)

        transform = np.transpose(transform)
        skimage.io.imsave(temp_image_dir + 'temp.jpg', transform)
        transform = skimage.io.imread(temp_image_dir + 'temp.jpg')
        return transform

    def read_input_npy(self, file_dir, file_name):

        sample_path = os.path.join(file_dir, 'inputs', file_name + '.npy')
        transform = np.load(sample_path)

        return transform

    def read_input(self, sample_name: str):

        sample_name = sample_name.replace('wav', 'png')
        spec_path = self.saved_transforms_directory + sample_name
        return skimage.io.imread(spec_path)

    def normalize_input(self, x: np.ndarray):
        # Since spectrograms are converted to skimages of type uint8, the max value is 255 and the min 0
        return (x - self.min_val) / (self.max_val - self.min_val)

    def get_full_transform(self, sample_name: str, calculate_input: bool):
        if calculate_input:
            transformed_wav = self.calculate_input(sample_name)
        else:
            transformed_wav = self.read_input(sample_name)

        return transformed_wav

    @abstractmethod
    def get_input(self, sample_name: str, calculate_input: bool, normalize_input: bool):
        return

    @abstractmethod
    def change_transform_shape(self, transformed_wav: np.ndarray):
        return

    @abstractmethod
    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        return
