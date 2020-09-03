import os
import pandas as pd
import numpy as np
from statistics import mean, variance, stdev
from scipy.stats import variation


def store_sorted_metrics(metrics_dir: str, time_size: int, metrics: list):
    metrics.sort(key=lambda tup: tup[1])
    file_path = os.path.join(metrics_dir, 'sort_by_mean_time_size_' + str(time_size) + '.txt')
    with open(file_path, 'w') as f:
        for offset_metrics in metrics:
            f.write(str(offset_metrics) + '\n')

    metrics.sort(key=lambda tup: tup[2])
    file_path = os.path.join(metrics_dir, 'sort_by_variance_time_size_' + str(time_size) + '.txt')
    with open(file_path, 'w') as f:
        for offset_metrics in metrics:
            f.write(str(offset_metrics) + '\n')

    metrics.sort(key=lambda tup: tup[3])
    file_path = os.path.join(metrics_dir, 'sort_by_stdev_time_size_' + str(time_size) + '.txt')
    with open(file_path, 'w') as f:
        for offset_metrics in metrics:
            f.write(str(offset_metrics) + '\n')

    metrics.sort(key=lambda tup: tup[4])
    file_path = os.path.join(metrics_dir, 'sort_by_coef_of_variation_time_size_' + str(time_size) + '.txt')
    with open(file_path, 'w') as f:
        for offset_metrics in metrics:
            f.write(str(offset_metrics) + '\n')


def get_metrics(data: np.ndarray, offset_step: int):
    x = data[:, 0]
    y = data[:, 1]
    coefficient_of_variation = stdev(y) / mean(y)
    tup = (offset_step, mean(y), variance(y), stdev(y), coefficient_of_variation)
    return tup


def read_class_counts_csv_as_dataframe(dataset_dir: str, time_size: int, offset_step: int):
    csv_dir = os.path.join(dataset_dir, 'class_counts', 'time_size_' + str(time_size))
    csv_name = 'offset_step_' + str(offset_step) + '.csv'
    csv_path = os.path.join(csv_dir, csv_name)
    df = pd.read_csv(csv_path)
    return df


def print_metrics(data: np.ndarray, offset_step: int):
    x = data[:, 0]
    y = data[:, 1]
    print('offset_step:', offset_step,
          'Mean:', mean(y),
          'Variance:', variance(y),
          'Standard Deviation:', stdev(y),
          'Coefficient of variation-statistics:', stdev(y) / mean(y),
          'Coefficient of variation-scipy:', variation(y))
