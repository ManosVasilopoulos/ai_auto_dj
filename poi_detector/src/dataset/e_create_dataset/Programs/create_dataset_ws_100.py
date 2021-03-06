from poi_detector.src.basic_classes.helper import get_data_from_csv
from poi_detector.src.basic_classes.constants import relative_locator_csv_path
from poi_detector.src.dataset.e_create_dataset.Classes.input_handler import InputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.output_handler import OutputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.data_balancer import DatasetBalancer
from os.path import join as os_path_join

base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
transform_type = 'spectrogram'
time_size = 1000
freq_size = 20
window_size = 100

dataset_dir = os_path_join(base_dir, str(window_size))
input_handler = InputDatasetHandler(transform_type, window_size)
output_handler = OutputDatasetHandler(window_size)
balancer = DatasetBalancer()

names, pois_lists = get_data_from_csv(relative_locator_csv_path)

n_samples = names.shape[0]
i = 0
for name, pois_list in zip(names, pois_lists):
    i += 1
    try:
        print('Trying', i, 'out of', n_samples, '.')

        """ CREATE SPECTROGRAM """
        spectrogram = input_handler.calculate_input(name, 'spectrogram', 512)
        balancer.save_input(dataset_dir, name + 'spectrogram', spectrogram)

        """ CREATE MEL-SPECTROGRAM """
        melspectrogram = input_handler.calculate_input(name, 'melspectrogram', 256)
        balancer.save_input(dataset_dir, name + 'melspectrogram', melspectrogram)

        """ CREATE MFCC """
        mfcc = input_handler.calculate_input(name, 'mfcc', 20)
        balancer.save_input(dataset_dir, name + 'mfcc', mfcc)

        """ CREATE ONE-VECTOR-OUTPUT AND RAW OUTPUT """
        one_hot_vector = output_handler.list_to_vector(pois_list, spectrogram.shape[0])
        balancer.save_output(dataset_dir, name, one_hot_vector, pois_list)

    except Exception as e:
        print('Failed', name, 'Error', e)
        continue
    except KeyboardInterrupt:
        break
