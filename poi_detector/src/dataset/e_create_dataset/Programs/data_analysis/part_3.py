"""
For every exported file of "part_2.py" a figure is created.
Each figure plots the number of instances of each class.
We can see the distribution of the dataset with this approach.
"""
from .helpers.part_3_helper import read_class_counts_csv_as_dataframe, create_and_save_plot
from .constants import base_dir
import os

time_sizes = [100, 250, 500, 1000]
transform_type = 'cqt'
window_size = 11.61
dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))

os.system('cls')
try:
    os.mkdir(os.path.join(dataset_dir, 'plots'))
except:
    print('Directory already exists. Skipping making dir...')

offset_steps = [i for i in range(50, 100)]

for time_size in time_sizes:
    for offset_step in offset_steps:
        df = read_class_counts_csv_as_dataframe(dataset_dir, time_size, offset_step)

        data = df.to_numpy()

        create_and_save_plot(dataset_dir, data, time_size, offset_step)

