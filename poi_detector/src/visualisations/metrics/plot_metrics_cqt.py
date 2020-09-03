from .constants_metrics import project_dir
from .helper import turn_names_to_paths, get_metrics_dict, pad_metrics_dict, plot_metrics
import os
import sys


def main():
    st = 'Preciser v1'
    tt = 'cqt'
    window_size = 11.61
    m_id = 8
    time_size = 100

    model_dir = os.path.join(project_dir, st, str(m_id), tt, str(window_size), str(time_size))
    train_dir = os.path.join(model_dir, 'Train')
    test_dir = os.path.join(model_dir, 'Test')

    train_metrics = os.listdir(train_dir)
    train_metrics = turn_names_to_paths(train_metrics, train_dir)
    train_metrics.sort(key=os.path.getmtime)
    train_metrics_dict, n_train = get_metrics_dict(train_metrics)

    test_metrics = os.listdir(test_dir)
    test_metrics = turn_names_to_paths(test_metrics, test_dir)
    test_metrics.sort(key=os.path.getmtime)
    test_metrics_dict, n_test = get_metrics_dict(test_metrics)
    test_metrics_dict = pad_metrics_dict(test_metrics_dict, n_train, n_test)

    plot_metrics(model_dir, train_metrics_dict, test_metrics_dict)


if __name__ == '__main__':
    main()
