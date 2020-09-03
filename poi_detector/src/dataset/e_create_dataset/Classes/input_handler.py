import numpy as np

from poi_detector.src.basic_classes.input_handler import InputHandler


class InputDatasetHandler(InputHandler):
    song_length = 0

    def get_input(self, sample_name: str, calculate_input: bool, normalize_input: bool):
        raise Exception('InputDatasetHandler Error: "get_input" has not been implemented.')

    def change_transform_shape(self, transformed_wav: np.ndarray):
        raise Exception('InputDatasetHandler Error: "change_transform_shape" has not been implemented.')

    def zero_pad_spectrogram(self, transformed_wav: np.ndarray):
        raise Exception('InputDatasetHandler Error: "zero_pad_spectrogram" has not been implemented.')
