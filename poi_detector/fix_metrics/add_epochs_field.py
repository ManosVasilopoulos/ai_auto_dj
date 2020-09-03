import pickle
import numpy
import matplotlib.pyplot as plt
import os
import sys

project_dir = 'D:/Documents/Thesis/Project Skaterbot/Good Neural Networks/'
visuals_dir = 'D:/Documents/Thesis/Project Skaterbot/Visuals/model results/'


def add_epoch(metrics_dict, metrics_path):
    if 'ep_0' in metrics_path:
        metrics_dict['epoch'] = 1
    if 'ep_1' in metrics_path:
        metrics_dict['epoch'] = 2
    if 'ep_2' in metrics_path:
        metrics_dict['epoch'] = 3
    if 'ep_3' in metrics_path:
        metrics_dict['epoch'] = 4
    if 'ep_4' in metrics_path:
        metrics_dict['epoch'] = 5
    if 'ep_5' in metrics_path:
        metrics_dict['epoch'] = 6
    if 'ep_6' in metrics_path:
        metrics_dict['epoch'] = 7
    if 'ep_7' in metrics_path:
        metrics_dict['epoch'] = 8
    if 'ep_8' in metrics_path:
        metrics_dict['epoch'] = 9
    if 'ep_9' in metrics_path:
        metrics_dict['epoch'] = 10
    return metrics_dict


def fix_metrics_and_save(metrics_paths, new_dir, old_dir, epoch):
    metrics = []
    for i, metrics_path in enumerate(metrics_paths):
        with open(metrics_path, 'rb') as f:
            # print('Opened: ' + metrics_path)
            temp_metrics = pickle.load(f)
        temp_metrics = add_epoch(temp_metrics, metrics_path)
        with open(new_dir + 'epoch_' + str(epoch) + '_' + str(i) + '.pkl', 'wb') as f:
            pickle.dump(temp_metrics, f, protocol=pickle.HIGHEST_PROTOCOL)


def turn_names_to_paths(filenames_list, directory):
    return [directory + filename for filename in filenames_list]


def main():
    model_dir = project_dir + 'Relative Locator/7/spectrogram/'
    history_dir = model_dir + 'History/'
    test_dir = model_dir + 'Test/'
    fixed_history_dir = model_dir + 'Fixed_History/'
    fixed_test_dir = model_dir + 'Fixed_Test/'

    for i in range(10):
        print('Epoch: ' + str(i + 1))
        history_ep_dir = history_dir + 'epoch ' + str(i + 1) + '/'
        train_metrics = os.listdir(history_ep_dir)
        train_metrics = turn_names_to_paths(train_metrics, history_ep_dir)
        train_metrics.sort(key=os.path.getmtime)

        fix_metrics_and_save(train_metrics, fixed_history_dir, history_ep_dir, i)

    test_metrics = os.listdir(test_dir)
    test_metrics = turn_names_to_paths(test_metrics, test_dir)
    test_metrics.sort(key=os.path.getctime)

    print()


if __name__ == '__main__':
    main()
