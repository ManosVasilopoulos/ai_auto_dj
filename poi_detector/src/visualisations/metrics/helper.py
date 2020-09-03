import pickle
import matplotlib.pyplot as plt
import sys
import numpy as np
from numpy import array as np_array
import os


def add_epoch_field(metrics_dict, metrics_path):
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


def get_number_of_metrics(sample_path):
    with open(sample_path, 'rb') as f:
        temp_metrics = pickle.load(f)
    return len(temp_metrics) - 2


def read_metrics(metrics_path):
    with open(metrics_path, 'rb') as f:
        # print('Opened: ' + metrics_path)
        temp_metrics = pickle.load(f)
    return temp_metrics


def get_metrics_names(sample_path):
    with open(sample_path, 'rb') as f:
        temp_metrics = pickle.load(f)

    metrics_names = []
    for metric in temp_metrics:
        if metric != 'id':
            metrics_names.append(metric)
    return metrics_names


def get_epoch(sample_path):
    with open(sample_path, 'rb') as f:
        temp_metrics = pickle.load(f)
    return temp_metrics['epoch']


def get_metrics_dict(metrics_paths):
    corrected_metrics = False
    metrics_dict = {}
    metrics_names = get_metrics_names(metrics_paths[0])
    if type(metrics_names[0]) != str:
        metrics_names = ['loss', 'binary_accuracy', 'mean_squared_error', 'mean_absolute_error']
        print('changed metrics_names')
        corrected_metrics = True

    for metric in metrics_names:
        if metric != 'model_name':
            metrics_dict[metric] = []

    # Append
    for metrics_path in metrics_paths:
        temp_metrics = read_metrics(metrics_path)
        for i, metric in enumerate(temp_metrics):
            if metric != 'id' and metric != 'model_name':
                if corrected_metrics and i > 3:
                    break
                metrics_dict[metrics_names[i]].append(temp_metrics[metric])

    for metric in metrics_dict:
        metrics_dict[metric] = np.array(metrics_dict[metric])

    n_samples = metrics_dict['loss'].shape[0]

    return metrics_dict, n_samples


def turn_names_to_paths(filenames_list, directory):
    return [os.path.join(directory, filename) for filename in filenames_list]


def make_epochs_list(n_samples, last_epoch):
    return np.linspace(0, last_epoch, n_samples)


def plot_metric(axes, y_train, metric_name, last_epoch, y_test=np_array([])):
    epochs_list = make_epochs_list(y_train.shape[0], last_epoch)
    x = epochs_list

    # alpha configures the amount of transparency of the line plotted
    axes.plot(x, y_train, 'b', scaley=True, label='Train')

    # axes.set_ylim(bottom=0, top=5)
    axes.set_ylabel(metric_name)
    axes.set_xlabel('Epoch')

    if y_test.any():
        # alpha configures the amount of transparency of the line plotted
        axes.plot(x, y_test, color='#FF9633', label='Test', alpha=0.85)
    axes.legend()


def plot_metrics(model_dir, train_metrics_dict, test_metrics_dict=None):
    metric_keys = list(train_metrics_dict)
    try:
        metric_keys.remove('epoch')
    except:
        pass
    last_epoch = train_metrics_dict['epoch'][-1]

    for i, key in enumerate(metric_keys):
        # fig, axis = plt.subplots(1, 1)
        fig = plt.figure(figsize=(13, 5))
        axes = plt.axes()
        if test_metrics_dict:
            plot_metric(axes,
                        train_metrics_dict[key],
                        key,
                        last_epoch,
                        y_test=test_metrics_dict[key],
                        )
        else:
            plot_metric(axes,
                        train_metrics_dict[key],
                        key,
                        last_epoch,
                        )
        try:
            os.mkdir(os.path.join(model_dir, 'plots'))
        except FileExistsError:
            pass
        plot_path = os.path.join(model_dir, 'plots', key + '.png')
        plt.savefig(plot_path)
        plt.close(fig)
    # plt.show()


def pad_metrics_dict2(test_metrics_dict, n_train, n_test):
    samples_per_sample = n_train // n_test
    new_metrics_dict = {}
    for metric in test_metrics_dict:
        new_test_samples = np.zeros((n_train,))
        for i in range(n_test):
            new_test_samples[i * samples_per_sample: (i + 1) * samples_per_sample] = test_metrics_dict[metric][i]
        new_metrics_dict[metric] = new_test_samples
    return new_metrics_dict


def pad_metrics_dict(test_metrics_dict, n_train, n_test):
    samples_per_sample = int(n_train // n_test + 1)
    new_metrics_dict = {}
    for metric in test_metrics_dict:
        new_test_samples = np.zeros((n_train,))
        for i in range(n_test):
            try:
                new_test_samples[i * samples_per_sample: (i + 1) * samples_per_sample] = test_metrics_dict[metric][i]
            except UnicodeDecodeError:
                break
        new_metrics_dict[metric] = new_test_samples
    return new_metrics_dict


def get_transform_type():
    while 1:
        try:
            tt = input('Choose transform type: ')
            failed_condition = tt != 'spectrogram' and tt != 'melspectrogram' and tt != 'mfcc'
            if failed_condition:
                print('Please choose one of the following transforms: (spectrogram, melspectrogram, mfcc) ')
            else:
                break
        except KeyboardInterrupt:
            sys.exit()
    return tt


def get_subsystem_type():
    while 1:
        try:
            subsystem_type = int(
                input("Enter '1' for 'Relative Locator' or '2' for 'Preciser': "))
            if not 1 <= subsystem_type <= 2:
                print("Wrong Subsystem Type. Please enter '1' or '2' only.")
                continue
            break
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print("Wrong Subsystem Type. Please enter '1' or '2' only.")

    if subsystem_type == 1:
        return 'Relative Locator'
    elif subsystem_type == 2:
        return 'Preciser'
    else:
        raise Exception('Something went wrong. Finishing program...')


def get_model_id():
    while 1:
        try:
            model_id = int(
                input("Choose a model starting from 1: "))
            if model_id < 1:
                print("Wrong Subsystem Type.")
                continue
            return model_id
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print("Wrong Subsystem Type.")


def split_train_val_metrics(train_val_metrics: dict):
    train_metrics_dict = {}
    val_metrics_dict = {}
    for metric_name in train_val_metrics:
        if 'val' in metric_name:
            val_metrics_dict[metric_name] = train_val_metrics[metric_name]
        else:
            train_metrics_dict[metric_name] = train_val_metrics[metric_name]

    val_metrics_dict['epoch'] = train_val_metrics['epoch']

    return train_metrics_dict, val_metrics_dict
