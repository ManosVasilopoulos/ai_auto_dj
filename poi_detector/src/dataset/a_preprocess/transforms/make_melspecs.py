from __future__ import absolute_import, division, print_function, unicode_literals
#from ..basic_classes.constants import wav_dir, preciser_csv_path, mels_dir
from poi_detector.src.basic_classes.constants import wav_dir, preciser_csv_path, mels_dir
from poi_detector.src.basic_classes.helper import get_data_from_csv
from poi_detector.src.basic_classes.transforms import calculate_transform
import numpy as np
import librosa
import pickle

""" Get Input-names and Output-Points of Interest """
# the last csv that is used has all songs shuffled. No need to process input names.
input_names, output_pois = get_data_from_csv(preciser_csv_path)
n_samples = input_names.shape[0]

transform_dir = mels_dir
failed = []
min_val = 1000000000000000000000000
max_val = -100000000000000000000000
for i in range(n_samples):
    sample_name = input_names[i]
    output_sample = output_pois[i]
    print(sample_name)

    try:
        wav, sr = librosa.load(wav_dir + sample_name, mono=True, sr=44100)

        transformed_x = calculate_transform(wav, sr, 'melspectrogram', 512)
        print(transformed_x.shape)
        print(min_val, max_val)
        trans_max = np.amax(transformed_x)
        if trans_max > max_val:
            max_val = trans_max
        trans_min = np.amin(transformed_x)
        if trans_min < min_val:
            min_val = trans_min
        print(trans_min, trans_max)
        print(min_val, max_val)
        print()
        with open(mels_dir + '512_mels/' + sample_name + '.pkl',
                  'wb') as pkl_file:

            pickle.dump(np.transpose(transformed_x), pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(transformed_x, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        failed.append(sample_name)
        continue


print('Max_value: ' + str(max_val))
print('Min_value: ' + str(min_val))
print('Failed:')
for fail in failed:
    print(fail)
with open(mels_dir + 'minmax.txt', 'wb') as f:
    f.write('Max: ' + str(max_val) + '\n')
    f.write('Min: ' + str(min_val))