from poi_detector.src.dataset.create_dataset.Classes.input_handler import InputDatasetHandler
from poi_detector.src.dataset.create_dataset.Classes.output_handler import OutputDatasetHandler
from poi_detector.src.dataset.create_dataset.Classes.data_balancer import DatasetBalancer
import os
import numpy as np

base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
transform_type = 'cqt'
window_size = 11.61

dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))
data_dir = os.path.join(dataset_dir, 'data')

input_handler = InputDatasetHandler(transform_type, window_size)
output_handler = OutputDatasetHandler(window_size)
balancer = DatasetBalancer()

names = os.listdir(data_dir)
n_samples = len(names)
i = 0
time_sizes = [100]
offset_steps = [83]
for time_size, offset_step in zip(time_sizes, offset_steps):

    print('Starting combination ---> (time_size, offset_step) = (' + str(time_size) + ', ' + str(offset_step) + ')')

    input_handler.set_time_size(time_size)
    output_handler.set_time_size(time_size)
    balancer.set_time_size(time_size)
    for name in names:
        i += 1
        try:
            sample_dir = os.path.join(data_dir, name)
            transform_path = os.path.join(sample_dir, 'inputs', name + transform_type + '.npy')
            transform = np.load(transform_path)

            one_hot_path = os.path.join(sample_dir, 'output', name + '.npy')
            one_hot_vector = np.load(one_hot_path)

            balancer.create_output_offsets(sample_dir, name, transform, one_hot_vector, offset_step)
            print('Finished', i, 'out of', n_samples)

        except Exception as e:
            print('Failed', name, 'Error', e)
            continue
        except KeyboardInterrupt:
            break
