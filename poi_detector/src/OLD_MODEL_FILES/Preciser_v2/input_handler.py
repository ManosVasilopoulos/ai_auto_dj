import numpy as np
from basic_classes.input_handler import InputHandler


class InputPreciserHandler(InputHandler):
    """
    This input handler is for 2D-Colvolutional Input Layers.
    """

    def get_input(self, sample_name, calculate_input, normalize_input):

        transform = self.get_full_transform(sample_name, calculate_input)

        transform = self.zero_pad_spectrogram(transform)

        transform = self.change_transform_shape(transform)

        if normalize_input:
            transform = self.normalize_input(transform)
        return transform

    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        rest = self.time_size - transformed_wav.shape[0] % self.time_size
        data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))
        return data

    def change_transform_shape(self, transformed_wav):
        """
        :param transformed_wav: 2d numpy array with the transformed signal, meaning the spectrogram, melspectrogram etc.
        :return:
        """
        return np.reshape(transformed_wav, (-1, self.time_size, self.freq_size, 1))

    @staticmethod
    def filter_subspectrograms(subspec_list: np.ndarray, idxs: list):
        x = []
        for i in range(len(idxs)):
            index = idxs[i]
            x.append(subspec_list[index])
        x = np.array(x)

        return x
