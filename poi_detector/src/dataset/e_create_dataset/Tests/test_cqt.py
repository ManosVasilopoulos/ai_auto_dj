from ..Classes.input_handler import InputDatasetHandler
from basic_classes.helper import get_data_from_csv
from basic_classes.constants import preciser_csv_path

base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
transform_type = 'cqt'
freq_size = 96
window_size = 11.61

input_handler = InputDatasetHandler(transform_type, window_size)

names, _ = get_data_from_csv(preciser_csv_path)

test_name = names[0]

n_samples = names.shape[0]
i = 0

audio, sr = input_handler.read_audio(test_name)
for i in range(50, 150):
    try:
        cqt = input_handler.calculate_input(test_name, 'cqt', i)
        print('Audio shape:', audio.shape, 'Audio duration:', audio.shape[0] / sr)
        print('Constant-Q:', cqt.shape, 'Calculated size of time dimension:', audio.shape[0] / 512)
    except:
        print('Value', i, 'failed')

