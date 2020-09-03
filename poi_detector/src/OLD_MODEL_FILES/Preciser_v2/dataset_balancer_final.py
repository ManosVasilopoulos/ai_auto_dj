import numpy as np
from basic_classes.input_handler import InputHandler
import random
from basic_classes import constants
from basic_classes.data_balancer import Balancer


class PreciserBalancer(Balancer):
    """
    This input handler is for 2D-Colvolutional Input Layers.
    """

    def change_transform_shape(self, transformed_wav):
        min_val = np.amin(transformed_wav)
        rest = self.time_size - transformed_wav.shape[0] % self.time_size
        data = np.pad(transformed_wav, ((0, rest), (0, 0)), 'constant', constant_values=((0, min_val), (0, 0)))

        return data

    def save_as_image(self, filename, x, name_extention):
        import matplotlib.pyplot as plt
        import librosa.display
        plt.figure(figsize=(7, 4))
        librosa.display.specshow(x[10000:10500, :], cmap='viridis', x_axis='mel', y_axis='time', sr=44100,
                                 fmax=44100 // 2)
        filename = filename.replace('.wav', name_extention + '.png')
        plt.title(filename)
        plt.savefig(constants.specs_dir + filename)

    def filter_inputs_outputs(self, semi_final_ins, semi_final_outs):
        final_ins = np.empty((0, self.time_size, self.freq_size, 1))
        final_outs = np.empty((0, self.time_size))

        for in_sample, out_sample in zip(semi_final_ins, semi_final_outs):
            if np.any(out_sample == 1):
                final_ins = np.append(final_ins, np.expand_dims(in_sample, axis=-1))
                final_outs = np.append(final_outs, out_sample)

        return final_ins, final_outs
