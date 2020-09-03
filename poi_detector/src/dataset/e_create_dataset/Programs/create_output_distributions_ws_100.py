from poi_detector.src.basic_classes.helper import get_data_from_csv
from poi_detector.src.basic_classes.constants import relative_locator_csv_path
from poi_detector.src.dataset.e_create_dataset.Classes.input_handler import InputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.output_handler import OutputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.data_balancer import DatasetBalancer
from poi_detector.src.dataset.e_create_dataset.helper import get_transform_shapes
from os.path import join as os_path_join

base_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Library\\'
transform_type = 'spectrogram'
time_size = 1000
freq_size = 20
window_size = 100

dataset_dir = os_path_join(base_dir, 'window_size_' + str(window_size))
spec_shapes_csv_path = os_path_join(dataset_dir, 'spec_shapes_ws_100.csv')

transforms_shapes_dict = get_transform_shapes(spec_shapes_csv_path)

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
        transform_time = transforms_shapes_dict[name][0]
        """ CREATE ONE-VECTOR-OUTPUT AND RAW OUTPUT """
        distribution_vector = output_handler.list_to_distribution_vector(pois_list, transform_time)
        balancer.save_output_distribution(os_path_join(dataset_dir, 'data', name), name, distribution_vector)
        print('Finished', name, '---->', transform_time)

    except Exception as e:
        print('Failed', name, 'Error', e)
        continue
    except KeyboardInterrupt:
        break
