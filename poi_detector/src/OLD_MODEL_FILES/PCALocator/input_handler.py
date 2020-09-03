import numpy as np
from basic_classes.input_handler import InputHandler
from basic_classes import constants


class InputPCALocatorHandler(InputHandler):
    """
    This input handler is for LSTM Input Layers.
    """

    def get_input(self, sample_name, calculate_input, normalize_input):
        transform = self.get_full_transform(sample_name, calculate_input)
        transform, last_subspec_id = self.zero_pad_spectrogram(transform)

        if normalize_input:
            transform = self.normalize_input(transform)

        transform = self.change_transform_shape(transform)
        return transform, last_subspec_id

    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        if transformed_wav.shape[0] < constants.MAX_SAMPLES:
            last_subspec_id = transformed_wav.shape[0] // constants.MAX_SAMPLES
            rest = constants.MAX_SAMPLES - transformed_wav.shape[1] % constants.MAX_SAMPLES
            data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))
        else:
            data = transformed_wav[:constants.MAX_SAMPLES, :]
            last_subspec_id = constants.MAX_SAMPLES // self.time_size - 1

        return data, last_subspec_id

    def change_transform_shape(self, transformed_wav):
        """
        :param transformed_wav: 2d numpy array with the transformed signal, meaning the spectrogram, melspectrogram etc.
        :return:
        """

        return np.reshape(transformed_wav, (-1, self.time_size * self.freq_size))
