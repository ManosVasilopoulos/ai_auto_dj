from os.path import join as os_path_join
from os import listdir as os_listdir

base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
transform_type = 'spectrogram'
time_size = 1000
freq_size = 20
window_size = 10

dataset_dir = os_path_join(base_dir, str(window_size))
names = os_listdir(dataset_dir)

n_samples = len(names)
i = 0
for name in names:
    i += 1
    try:

        print('Trying', i, 'out of', n_samples, ':', name)

        # DELETE OFFSETS
        offsets_dir = os.path.join(dataset_dir, name, 'offsets')
        offsets_files_list = os.listdir(offsets_dir)
        for offset_file in offsets_files_list:
            os.remove(os.path.join(offsets_dir, offset_file))
    except Exception as e:
        print('Failed', name, 'Error', e)
        continue
    except KeyboardInterrupt:
        break
