from __future__ import absolute_import, division, print_function, unicode_literals
from poi_detector.src.basic_classes.constants import preciser_csv_path, mfcc_dir, mels_dir
from poi_detector.src.basic_classes.helper import get_data_from_csv
import numpy as np
import librosa
import matplotlib.pyplot as plt
import pickle

""" Get Input-names and Output-Points of Interest """
# the last csv that is used has all songs shuffled. No need to process input names.
input_names, output_pois = get_data_from_csv(preciser_csv_path)
n_samples = input_names.shape[0]

failed = []

min_val = 1000000000000000000000000
max_val = -100000000000000000000000

for i in range(n_samples):
    sample_name = input_names[i]
    output_sample = output_pois[i]
    print(sample_name)

    try:

        sample_name += '.pkl'
        with (open(mels_dir + '512_mels/' + sample_name, "rb")) as openfile:
            in_data = pickle.load(openfile)

        x = librosa.feature.mfcc(S=in_data, sr=44100, n_mfcc=20)

        plt.imshow(np.transpose(x[10000:10100, :]))
        print(x.shape)
        print(np.amax(x), np.amin(x))
        trans_max = np.amax(x)
        if trans_max > max_val:
            max_val = trans_max
        trans_min = np.amin(x)
        if trans_min < min_val:
            min_val = trans_min
        print(trans_min, trans_max)
        print(min_val, max_val)
        print()
        with open(mfcc_dir + '20_cc/' + sample_name + '.pkl',
                  'wb') as output:
            pickle.dump(np.transpose(x), output, pickle.HIGHEST_PROTOCOL)

    except Exception as e:
        print(e)

        failed.append(sample_name)
    break

print('Failed:')
for fail in failed:
    print(fail)

with open(mfcc_dir + 'minmax.txt', 'w+') as f:
    f.write('Max: ' + str(max_val) + '\n')
    f.write('Min: ' + str(min_val))
