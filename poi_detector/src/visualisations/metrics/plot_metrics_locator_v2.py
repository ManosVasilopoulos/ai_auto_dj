from .constants_metrics import project_dir
from .helper import turn_names_to_paths, get_metrics_dict, pad_metrics_dict, plot_metrics, split_train_val_metrics
import os
import sys


def main(arg_list):
    if not arg_list:
        raise Exception('This program needs one argument: "id".')
    st = 'Relative Locator v2'
    tt = 'melspectrogram'
    window_size = 100
    time_size = 1000
    m_id = int(arg_list[0])

    if not 0 < m_id <= 10:
        raise Exception("The model's ID needs a value between 0 and 10")
    if time_size != 100 and time_size != 250 and time_size != 500 and time_size != 1000:
        raise Exception("The model's \"time_size\" needs a value between 0 and 10")

    model_dir = os.path.join(project_dir, st, str(m_id), tt, str(window_size), str(time_size))
    train_dir = os.path.join(model_dir, 'Train')
    test_dir = os.path.join(model_dir, 'Test')

    train_metrics = os.listdir(train_dir)
    train_metrics = turn_names_to_paths(train_metrics, train_dir)
    train_metrics.sort(key=os.path.getmtime)
    train_metrics_dict, n_train = get_metrics_dict(train_metrics)

    train_metrics_dict, val_metrics_dict = split_train_val_metrics(train_metrics_dict)

    test_metrics = os.listdir(test_dir)
    test_metrics = turn_names_to_paths(test_metrics, test_dir)
    test_metrics.sort(key=os.path.getmtime)
    test_metrics_dict, n_test = get_metrics_dict(test_metrics)
    test_metrics_dict = pad_metrics_dict(test_metrics_dict, n_train, n_test)

    plot_metrics(model_dir, train_metrics_dict, test_metrics_dict)

    if bool(val_metrics_dict):
        plot_metrics(model_dir, val_metrics_dict)

if __name__ == '__main__':
    main(sys.argv[1:])
