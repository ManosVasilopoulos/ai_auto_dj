import numpy as np
from basic_classes.constants import MAX_SAMPLES
from basic_classes.input_handler import InputHandler


class InputLocatorHandler(InputHandler):
    """
    This input handler is for LSTM Input Layers.
    """

    def change_transform_shape(self, transformed_wav):
        """
        :param transformed_wav: 2d numpy array with the transformed signal, meaning the spectrogram, melspectrogram etc.
        :return:
        """
        if transformed_wav.shape[0] < MAX_SAMPLES:
            last_subspec_id = transformed_wav.shape[0] // self.time_size
            rest = MAX_SAMPLES - transformed_wav.shape[0] % MAX_SAMPLES
            data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))
        else:
            last_subspec_id = MAX_SAMPLES // self.time_size - 1
            data = transformed_wav[:MAX_SAMPLES, :]

        data = np.reshape(data, (-1, self.time_size, self.freq_size))

        return data, last_subspec_id
