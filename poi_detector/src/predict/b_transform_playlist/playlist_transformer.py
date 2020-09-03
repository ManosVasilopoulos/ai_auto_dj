from os import listdir as os_listdir
from os.path import join as os_path_join
from poi_detector.src.basic_classes.transforms2 import Transform
from librosa import load as librosa_load
from skimage.io import imsave
from poi_detector.src.predict.helper import create_sub_dir
from poi_detector.src.predict.helper import keep_files
from numpy import transpose as np_transpose


def transform_playlist(wav_directory: str):
    wav_list = keep_files(os_listdir(wav_directory), 'wav')

    transformer = Transform()

    transforms_dir = create_sub_dir(wav_directory, 'transforms')

    transforms_sub_dirs = ['preciser_spectrogram', 'preciser_melspectrogram', 'preciser_cqt', 'locator_v1_cqt',
                           'locator_v2_spectrogram', 'locator_v2_melspectrogram']
    for sub_dir in transforms_sub_dirs:
        create_sub_dir(transforms_dir, sub_dir)

    for wav_file in wav_list:
        samples, sample_rate = librosa_load(os_path_join(wav_directory, wav_file), mono=True, sr=44100)

        preciser_spectrogram = transformer.get_spectrogram(sample_rate, samples, 10, 512)
        preciser_melspectrogram = transformer.get_melspectrogram(sample_rate, samples, 10, 256)
        preciser_cqt = transformer.get_constant_q(sample_rate, samples, 108)

        locator_v1_cqt = transformer.get_constant_q(sample_rate, samples, 108)

        locator_v2_spectrogram = transformer.get_spectrogram(sample_rate, samples, 100, 4411)
        locator_v2_melspectrogram = transformer.get_melspectrogram(sample_rate, samples, 100, 256)

        transforms = {'preciser_spectrogram': preciser_spectrogram,
                      'preciser_melspectrogram': preciser_melspectrogram,
                      'preciser_cqt': preciser_cqt,
                      'locator_v1_cqt': locator_v1_cqt,
                      'locator_v2_spectrogram': locator_v2_spectrogram,
                      'locator_v2_melspectrogram': locator_v2_melspectrogram}

        for transform in transforms:
            imsave(
                os_path_join(
                    transforms_dir,
                    transform,
                    wav_file + '.jpg'),
                np_transpose(transforms[transform])
            )
            print('Saved', wav_file + '.jpg')
