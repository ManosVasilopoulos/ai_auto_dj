import os
import pandas as pd

time_sizes = [500, 1000]
ws = 100
base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
dataset_dir = os.path.join(base_dir, 'window_size_' + str(ws))
data_dir = os.path.join(dataset_dir, 'data')
songs_list = os.listdir(data_dir)

samples = {}
counter = 1
for time_size in time_sizes:
    for i, song in enumerate(songs_list):
        offsets_song_path = os.path.join(data_dir, song, 'offsets', 'time_size_' + str(time_size))
        offsets_names = os.listdir(offsets_song_path)
        for j, offset_name in enumerate(offsets_names):
            samples[str(counter)] = offset_name
            counter += 1
        print('Finished', i, 'samples.')
    df = pd.DataFrame.from_dict(samples, orient="index")
    df.to_csv(os.path.join(dataset_dir, 'offsets_list_ts' + str(time_size) + '.csv'))
