import os
import pandas as pd
import matplotlib.pyplot as plt


def read_class_counts_csv_as_dataframe(dataset_dir: str, time_size: int, offset_step: int):
    time_dir = os.path.join(dataset_dir, 'class_counts', 'time_size_' + str(time_size))
    csv_name = 'offset_step_' + str(offset_step) + '.csv'
    csv_path = os.path.join(time_dir, csv_name)

    df = pd.read_csv(csv_path)
    return df


def create_and_save_plot(dataset_dir, data, time_size, offset_step):
    plot_name = 'time_size_'+str(time_size) + '_offset_step_'+str(offset_step)

    x = data[:, 0]
    y = data[:, 1]
    fig = plt.figure(figsize=(15.4, 5.5))
    plt.bar(x, y, align='center')  # A bar chart
    plt.title(plot_name)

    jpg_time_dir = os.path.join(dataset_dir, 'plots', 'time_size_' + str(time_size))
    try:
        os.mkdir(jpg_time_dir)
    except FileExistsError:
        pass

    jpg_path = os.path.join(jpg_time_dir, 'offset_step_'+str(offset_step) + '.jpg')
    plt.savefig(jpg_path)
    plt.close(fig)
