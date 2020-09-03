from .neural_networks import RNN
import os

_id = 1
window_size = 100
time_size = 1000
freq_size = 4411
transform_type = 'spectrogram'
model_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Good Neural Networks\\Relative Locator v2\\' + str(
    _id) + '\\' + transform_type + '\\' + str(window_size) + '\\' + str(time_size)
model_txt_path = os.path.join(model_dir, 'model_summary.txt')


def write_to_txt(summary):
    with open(model_txt_path, 'a') as f:
        f.write(summary + '\n')


rnn = RNN(_id, transform_type, window_size, time_size, freq_size)

rnn.decoder.summary(print_fn=write_to_txt)
