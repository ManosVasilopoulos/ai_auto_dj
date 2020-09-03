from poi_detector.src.basic_classes.helper import get_data_from_csv
from poi_detector.src.basic_classes.constants import preciser_csv_path
from poi_detector.src.dataset.e_create_dataset.Classes.input_handler import InputDatasetHandler
from os.path import join as os_path_join
from os import mkdir as os_mkdir
from random import randint
from poi_detector.src.basic_classes.transforms import Transform
import librosa
from poi_detector.src.basic_classes.constants import wav_dir
from os.path import join as ospathjoin
import skimage.io
import numpy as np

base_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/Library/'
transform_type = 'cqt'
freq_size = 512
window_size = 10

dataset_dir = os_path_join(base_dir, 'window_size_' + str(window_size))
data_dir = os_path_join(dataset_dir, 'data')

try:
    os_mkdir(data_dir)
except FileExistsError:
    pass

input_handler = InputDatasetHandler(transform_type, window_size)
names, pois_lists = get_data_from_csv(preciser_csv_path)

sample_name = names[randint(0, names.shape[0])]

try:
    print('Trying:', sample_name)

    """ CREATE CQT """
    audio_data, sr = librosa.load(ospathjoin(wav_dir, sample_name), sr=44100)

    spectrogram = Transform.get_bad_spectrogram(audio_data, sr, freq_size, window_size)
    spectrogram = np.flip(spectrogram, axis=0)
    spec_dir = 'D:\Documents\Thesis\THESIS CHAPTERS\Chapter 2 - AUDIO AND TRANSFORMS'
    spec_path = ospathjoin(spec_dir, sample_name)
    skimage.io.imsave(spec_path + '_bad.jpg', spectrogram[:, 1000: 1512])

    spectrogram = Transform.get_good_spectrogram(audio_data, sr, freq_size, window_size)
    spectrogram = np.flip(spectrogram, axis=0)
    spec_dir = 'D:\Documents\Thesis\THESIS CHAPTERS\Chapter 2 - AUDIO AND TRANSFORMS'
    spec_path = ospathjoin(spec_dir, sample_name)
    skimage.io.imsave(spec_path + '_good.jpg', spectrogram[:, 1000: 1512])


except Exception as e:
    print('Failed', sample_name, 'Error', e)
