"""
Calculate covariances
"""
from .helpers.part_4_helper import read_class_counts_csv_as_dataframe, print_metrics, get_metrics, store_sorted_metrics
from .constants import base_dir
import os

time_sizes = [100, 250, 500, 1000]
window_size = 11.61
dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))
metrics_dir = os.path.join(dataset_dir, 'metrics')

os.system('cls')
try:
    os.mkdir(metrics_dir)
except:
    print('Directory already exists. Skipping making dir...')

offset_steps = [i for i in range(50, 100)]

for time_size in time_sizes:
    metrics = []
    for offset_step in offset_steps:
        df = read_class_counts_csv_as_dataframe(dataset_dir, time_size, offset_step)
        data = df.to_numpy()

        #print_metrics(data, offset_step)

        metrics.append(get_metrics(data, offset_step))

    store_sorted_metrics(metrics_dir, time_size, metrics)
