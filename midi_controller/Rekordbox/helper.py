from constants import csv_path, bpm_path
import csv
import numpy as np

def get_playlist_points(names_only=False):
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

def get_bpm_of_tracks(names_only=False):
    input_names = []
    bpms = []
    with open(bpm_path, encoding='ISO-8859-1') as csvfile:
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
                bpms.append(csv_row)
            else:
                print('SKIPPED POIS of: ')
                print(audio_name + '\n')

    if not names_only:
        if len(input_names) != len(bpms):
            print('SOMETHING WENT WRONG\nInput and Output sizes don\'t match.')
            raise Exception('Exiting...')
    input_names = np.array(input_names)
    bpms = np.array(bpms)

    return input_names, bpms
