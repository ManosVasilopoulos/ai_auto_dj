"""
This programs reads the exported csv of "part_1.py".
This file contains the durations of all the spectrograms.
The program finishes with exporting 50 csv files each containing the counts of each class which is
a result of the offset_step.
"""
from poi_detector.src.dataset.e_create_dataset.Programs.data_analysis.helpers.part_2_helper import get_global_counts, \
    transform_np_array_to_dict, save_dict_to_csv, csv_to_numpy
from poi_detector.src.dataset.e_create_dataset.Classes.output_handler import OutputDatasetHandler
from poi_detector.src.dataset.e_create_dataset.Classes.data_balancer import DatasetBalancer
from .constants import base_dir
import os

# Variables
transform_type = 'cqt'
window_size = 11.61
dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))
data_dir = os.path.join(dataset_dir, 'data')

os.system('cls')

# Create 'class_counts_per_offset' folder.
try:
    os.mkdir(os.path.join(dataset_dir, 'class_counts'))
except:
    print('Directory already exists. Skipping making dir...')

shapes_list = csv_to_numpy(os.path.join(dataset_dir, 'spec_shapes_ws_' + str(window_size) + '.csv'))

offset_steps = [i for i in range(50, 100)]

output_handler = OutputDatasetHandler(window_size)
balancer = DatasetBalancer()

time_sizes = [100, 250, 500, 1000]
for time_size in time_sizes:

    output_handler.set_time_size(time_size)
    balancer.set_time_size(time_size)
    for offset_step in offset_steps:
        print('Time size:', time_size, 'Offset_step:', offset_step)

        global_out_counter = get_global_counts(dataset_dir, shapes_list, balancer, output_handler, offset_step, time_size)

        dict_ = transform_np_array_to_dict(global_out_counter, time_size)

        save_dict_to_csv(dataset_dir, time_size, offset_step, dict_)
