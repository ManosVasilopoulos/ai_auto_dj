from .neural_networks import CNN
import os

_id = 7
window_size = 100
time_size = 1000
freq_size = 256
transform_type = 'melspectrogram'
model_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Good Neural Networks\\Relative Locator v2\\' + str(
    _id) + '\\' + transform_type + '\\' + str(window_size) + '\\' + str(time_size)
model_txt_path = os.path.join(model_dir, 'model_summary.txt')


def write_to_txt(summary):
    with open(model_txt_path, 'a') as f:
        f.write(summary + '\n')


cnn = CNN(_id)
model, _ = cnn.get_model(time_size, freq_size)

model.summary()
