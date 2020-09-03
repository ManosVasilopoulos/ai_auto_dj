import numpy as np
from basic_classes.input_handler import InputHandler
import random
from basic_classes import constants
import skimage.io


class TestPreciserBalancer(InputHandler):
    """
    This input handler is for 2D-Colvolutional Input Layers.
    """

    def change_transform_shape(self, transformed_wav):
        min_val = np.amin(transformed_wav)
        rest = self.time_size - transformed_wav.shape[0] % self.time_size
        data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, min_val), (0, 0)))

        return data

    def get_input(self, sample_name, calculate_input, normalize_input):
        if calculate_input:
            transform = self.calculate_input(sample_name)
        else:
            transform = np.transpose(self.read_input(sample_name))

        transform = self.change_transform_shape(transform)
        return transform

    def get_input_output(self, sample_name: str, calculate_input: bool, normalize_input: bool, sample_pois: list):
        transform = self.get_input(sample_name, calculate_input, normalize_input)
        # print('Transform Shape: ' + str(transform.shape))
        x_all = np.empty((0, self.time_size, self.freq_size, 1))
        y_all = np.empty((0, 1))
        for poi in sample_pois:
            x_s, y_s = self.get_extra_input_output(sample_name, transform, poi)
            x_all = np.append(x_all, x_s, axis=0)
            y_all = np.append(y_all, y_s, axis=0)

        # print('x_all Shape: ' + str(x_all.shape), 'y_all Shape: ' + str(y_all.shape))
        return x_all, y_all

    def get_extra_input_output(self, sample_name: str, transform: np.ndarray, poi: int):

        temp_dir = 'D:/Documents/Thesis/Saved Transforms/Temp/'

        transform_duration = transform.shape[0] / (1000 // self.window_size)
        frame_seconds = self.time_size / (1000 // self.window_size)

        if poi < frame_seconds:
            poi_idx = int((poi % frame_seconds) * (1000 // self.window_size))
            y = np.array([poi_idx - 1])
            x_s = np.expand_dims(transform[:self.time_size, :], axis=0)
            x_s = np.expand_dims(x_s, axis=-1)
            y_s = np.expand_dims(y, axis=0)
        elif transform_duration - poi < frame_seconds:
            poi_idx = int((poi % frame_seconds) * (1000 // self.window_size))
            y = np.array([poi_idx - 1])
            x_s = np.expand_dims(transform[-self.time_size:, :], axis=0)
            x_s = np.expand_dims(x_s, axis=-1)
            y_s = np.expand_dims(y, axis=0)
        else:
            x_s = np.empty((0, self.time_size, self.freq_size, 1))
            y_s = np.empty((0, 1))
            poi_idx = int(poi * (1000 // self.window_size))
            res = [random.randrange(0, self.time_size - 1, 1) for p in range(10)]
            # print('POI: ' + str(poi))
            for i in res:
                frame_start = poi_idx - i - 1
                frame_end = poi_idx - i - 1 + self.time_size

                x = transform[frame_start:frame_end]
                y_pos = poi_idx - frame_start

                x[y_pos] = 255
                x = np.transpose(x)
                im_name = sample_name.replace('.wav', str(i) + '.jpg')
                skimage.io.imsave(temp_dir + im_name, x)
        return x_s, y_s

    def save_as_image(self, filename: str, x: np.ndarray, name_extention=''):
        import matplotlib.pyplot as plt
        import librosa.display
        plt.figure(figsize=(7, 4))
        librosa.display.specshow(x[10000:10500, :], cmap='viridis', x_axis='mel', y_axis='time', sr=44100,
                                 fmax=44100 // 2)
        filename = filename.replace('.wav', name_extention + '.png')
        plt.title(filename)
        plt.savefig(constants.specs_dir + filename)
