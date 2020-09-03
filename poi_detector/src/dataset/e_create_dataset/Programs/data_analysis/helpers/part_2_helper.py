import numpy as np
import os
from poi_detector.src.dataset.create_dataset.Classes.output_handler import OutputDatasetHandler
from poi_detector.src.dataset.create_dataset.Classes.data_balancer import DatasetBalancer
import pandas as pd

def csv_to_numpy(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_numpy()


def get_list_of_pois(songs_list: list, data_dir: str):
    db = {}
    for song in songs_list:
        pois = np.load(os.path.join(data_dir, song, 'output_raw', song))
        db[song] = pois
    return db
def two_arrays_to_dict(arr1: np.ndarray, arr2: np.ndarray):
    dict_ = {}

    for x, y in zip(arr1, arr2):
        dict_[x] = y

    return dict_

def save_dict_to_csv(dataset_dir: str, time_size: int, offset_step: int, dict_: dict):
    df = pd.DataFrame.from_dict(dict_, orient="index")

    new_time_dir = os.path.join(dataset_dir, 'class_counts', 'time_size_' + str(time_size))
    try:
        os.mkdir(new_time_dir)
    except FileExistsError:
        pass
    class_counts_path = os.path.join(new_time_dir, 'offset_step_' + str(offset_step) + '.csv')
    df.to_csv(class_counts_path)


def transform_np_array_to_dict(global_out_counter: np.ndarray, time_size: int):
    dict_ = {}
    for j in range(time_size):
        dict_[str(j)] = global_out_counter[j]
    return dict_


def get_global_counts(dataset_dir: str, shapes_list: np.ndarray, balancer: DatasetBalancer,
                      output_handler: OutputDatasetHandler, offset_step: int, time_size: int):

    data_dir = os.path.join(dataset_dir, 'data')

    succesful = 0
    fails = 0
    global_out_counter = np.zeros(time_size)
    for song_n_shape in shapes_list:

        song = song_n_shape[0]
        duration = song_n_shape[1]

        try:
            pois_list = np.load(os.path.join(data_dir, song, 'output_raw', song + '.npy'))
        except FileNotFoundError:
            fails += 1
            continue
        one_hot_vector = output_handler.list_to_vector(pois_list, duration)

        global_out_counter += balancer.get_samples_pois_counts(one_hot_vector, offset_step)
        succesful += 1
    print('Number of fails:', fails)
    print('Number of successes:', succesful)
    return global_out_counter
