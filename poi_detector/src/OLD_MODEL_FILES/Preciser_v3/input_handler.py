import numpy as np
from basic_classes.input_handler import InputHandler


class InputPreciserHandler(InputHandler):
    """
    This input handler is for 2D-Colvolutional Input Layers.
    """

    def get_input(self, sample_name, calculate_input, normalize_input):
        transform = self.get_full_transform(sample_name, calculate_input)

        if normalize_input:
            transform = self.normalize_input(transform)

        transform = self.change_transform_shape(transform)

        return transform

    def __get_shaped_input(self, transformed_wav, extras=False):
        """
                :param transformed_wav: 2d numpy array with the transformed signal, meaning the spectrogram, melspectrogram etc.
                :return:
                """
        rest = self.time_size - transformed_wav.shape[0] % self.time_size
        data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))

        self.set_song_length(data.shape[0])

        final_in = np.empty((0, self.time_size, self.freq_size))

        if extras:
            step = 101
            i = 100
        else:
            step = self.time_size
            i = self.time_size

        while i < self.song_length - step:
            mid_in = data[i: i + self.time_size]
            final_in = np.append(final_in, mid_in)
            i += step

        last_in = data[-self.time_size:]
        final_in = np.append(final_in, last_in)

        return final_in

    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        rest = self.time_size - transformed_wav.shape[0] % self.time_size
        data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))

        self.set_song_length(data.shape[0])

        return data

    def change_transform_shape(self, transformed_wav):
        """
        :param transformed_wav: 2d numpy array with the transformed signal, meaning the spectrogram, melspectrogram etc.
        :return:
        """
        data = self.zero_pad_spectrogram(transformed_wav)
        final_in = np.empty((0, self.time_size, self.freq_size))

        step = self.time_size
        i = self.time_size

        while i < self.song_length - step:
            mid_in = data[i: i + self.time_size]
            final_in = np.append(final_in, mid_in)
            i += step

        last_in = data[-self.time_size:]
        final_in = np.append(final_in, last_in)

        return final_in
