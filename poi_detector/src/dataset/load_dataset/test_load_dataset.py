from .load_dataset import load_dataset

csv_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Relative Locator/spectrogram/window_size_100/time_size_1000/'
csv_path = csv_dir + 'offsets_list_dataset.csv'

load_dataset(csv_path, 'gg')
