from models.locator_v2.model import Locator2

dataset_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Relative Locator\\spectrogram\\window_size_100\\time_size_1000\\'
csv_name = 'offsets_list_dataset.csv'

_id = 7
batch_size = 1
time_size = 1000
freq_size = 256
transform_type = 'melspectrogram'
window_size = 100

locator = Locator2(_id, batch_size, time_size, freq_size, transform_type, window_size)
print(locator.loss, locator.metrics_names)
locator.cnn_model.summary()