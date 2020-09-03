from poi_detector.src.basic_classes.helper import get_data_from_csv
from poi_detector.src.basic_classes.constants import preciser_csv_path
from poi_detector.src.dataset.e_create_dataset.Classes.input_handler import InputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.output_handler import OutputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.data_balancer import DatasetBalancer
from os.path import join as os_path_join
from os import mkdir as os_mkdir

base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
transform_type = 'cqt'
freq_size = 108
window_size = 11.61

dataset_dir = os_path_join(base_dir, 'window_size_' + str(window_size))
data_dir = os_path_join(dataset_dir, 'data')

try:
    os_mkdir(data_dir)
except FileExistsError:
    pass

input_handler = InputDatasetHandler(transform_type, window_size)
output_handler = OutputDatasetHandler(window_size)
balancer = DatasetBalancer()

names, pois_lists = get_data_from_csv(preciser_csv_path)

n_samples = names.shape[0]
i = 0
for name, pois_list in zip(names, pois_lists):
    i += 1
    try:
        print('Trying', i, 'out of', n_samples, ':', name)
        song_dir = balancer.make_song_dir(data_dir, name)

        """ CREATE CQT """
        cqt = input_handler.calculate_input(name, 'cqt', freq_size)
        balancer.save_input(song_dir, name + 'cqt', cqt)
    except Exception as e:
        print('Failed', name, 'Error', e)
        continue
    except KeyboardInterrupt:
        break
