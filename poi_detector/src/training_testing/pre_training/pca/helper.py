from os.path import join as pathjoin
from os import mkdir
import numpy as np


def mk_pca_dir(pca_dir: str, transform_type: str, window_size: float, time_size: int, freq_size: int):
    transform_type_dir = pathjoin(pca_dir, transform_type)
    try:
        mkdir(transform_type_dir)
    except FileExistsError:
        pass

    window_size_dir = pathjoin(transform_type_dir, str(window_size))
    try:
        mkdir(window_size_dir)
    except FileExistsError:
        pass

    time_size_dir = pathjoin(window_size_dir, str(time_size))
    try:
        mkdir(time_size_dir)
    except FileExistsError:
        pass

    freq_size_dir = pathjoin(time_size_dir, str(freq_size))
    try:
        mkdir(freq_size_dir)
    except FileExistsError:
        pass

    return freq_size_dir


def get_pca_path(pca_dir: str, transform_type: str, window_size: float, time_size: int, freq_size: int):
    pca_dir = pathjoin(pca_dir, transform_type, str(window_size), str(time_size), str(freq_size))
    return pathjoin(pca_dir, 'pca_' + transform_type + '.joblib')


def transform_ims_to_vecs(x_train):
    n_samples = x_train.shape[0]
    dim_1 = x_train.shape[1]
    dim_2 = x_train.shape[2]

    vec_length = dim_1 * dim_2

    reshaped_samples = []
    for i in range(n_samples):
        reshaped_samples.append(np.reshape(x_train[i], vec_length))

    return np.array(reshaped_samples)
