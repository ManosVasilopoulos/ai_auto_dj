import numpy as np
import csv
import random
from datetime import datetime

dt = datetime.now()
current_day = str(dt.day)
current_month = str(dt.month)


def get_data_from_csv(csv_path, names_only=False):
    input_names = []
    outputs = []
    with open(csv_path, encoding='ISO-8859-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i_d, row in enumerate(spamreader):
            if row == []:
                continue

            # Get song-name from CSV
            # audio_name = get_audio_name(row[0])
            audio_name = row[0]
            input_names.append(audio_name)
            if not names_only:
                csv_row = eval(row[1])
                outputs.append(csv_row)
            else:
                print('SKIPPED POIS of: ')
                print(audio_name + '\n')

    if not names_only:
        if len(input_names) != len(outputs):
            print('SOMETHING WENT WRONG\nInput and Output sizes don\'t match.')
            raise Exception('Exiting...')
    input_names = np.array(input_names)
    outputs = np.array(outputs)
    return input_names, outputs


def shuffle_dataset(inputs, outputs):
    n = inputs.shape[0]
    new_inputs = []
    new_outputs = []
    indexes = [i for i in range(n)]
    random.shuffle(indexes)
    for index in indexes:
        new_inputs.append(inputs[index])
        new_outputs.append(outputs[index])

    return np.array(new_inputs), np.array(new_outputs)


def count_pois(output_handler, time_sz, dataset_names, dataset_pois):
    n_samples = dataset_names.shape[0]
    n_songs = n_samples // 7
    n_train = int(n_songs * 0.8 * 7)
    n_test = n_samples - n_train

    # training samples
    train_names = dataset_names[:n_train]
    train_pois = dataset_pois[:n_train]

    # test samples
    test_names = dataset_names[n_train:]
    test_pois = dataset_pois[n_train:]


    """ Training Section """
    y_all = np.zeros(time_sz)
    batch_count = 0
    for i in range(n_train):
        sample_name = train_names[i]
        output_sample = train_pois[i]
        try:
            y, idxs = output_handler.get_output(output_sample, unique_outs=True)

            y_all += y.sum(0)
            batch_count += 1
        except Exception as e:
            print(e)
            continue

    for i in range(n_test):
        sample_name = test_names[i]
        output_sample = test_pois[i]
        try:
            y, idxs = output_handler.get_output(output_sample, unique_outs=True)

            y_all += y.sum(0)
            batch_count += 1
        except Exception as e:
            print(e)
            continue
    y_remaining = np.amax(y_all) - y_all
    return y_all, y_remaining