import numpy as np

from basic_classes.input_handler import InputHandler


class InputLocatorHandler2(InputHandler):
    song_length = 0

    def get_input(self, sample_name: str, calculate_input: bool, normalize_input: bool):
        raise Exception('InputLocatorHandler2 Error: "get_input" has not been implemented.')

    def change_transform_shape(self, transformed_wav: np.ndarray):
        raise Exception('InputLocatorHandler2 Error: "change_transform_shape" has not been implemented.')

    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        if transformed_wav.shape[0] < 1000:
            rest = 1000 - transformed_wav.shape[0] % 1000
            data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, self.min_val), (0, 0)))

            self.set_song_length(data.shape[0])

            return data
