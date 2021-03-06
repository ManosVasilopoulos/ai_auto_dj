import numpy as np
from basic_classes.input_handler import InputHandler


class InputPreciserHandler(InputHandler):
    """
    This input handler is for 2D-Colvolutional Input Layers.
    """

    def get_input(self, sample_name, calculate_input, normalize_input):

        transform = self.get_full_transform(sample_name, calculate_input)

        transform = self.zero_pad_spectrogram(transform)

        if normalize_input:
            transform = self.normalize_input(transform)

        transform = self.change_transform_shape(transform)
        return transform

    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        rest = self.time_size - transformed_wav.shape[0] % self.time_size
        padded_transform = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))
        return padded_transform

    def change_transform_shape(self, transformed_wav):
        """
        :param transformed_wav: 2d numpy array with the transformed signal, meaning the spectrogram, melspectrogram etc.
        :return:
        """
        return np.reshape(transformed_wav, (-1, self.time_size, self.freq_size, 1))

    @staticmethod
    def filter_subspectrograms(subspec_list, idxs=None):
        if idxs is None:
            raise Exception(
                'InputPreciserHandlerError: Please provide a list of indexes. "idxs" cannot be not specified.')
        x = []
        for i in range(len(idxs)):
            index = idxs[i]
            x.append(subspec_list[index])
        x = np.array(x)

        return x
