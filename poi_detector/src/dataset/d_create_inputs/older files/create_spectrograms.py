from basic_classes.constants import wav_dir
import os
from basic_classes.transforms import Transform
import librosa
from .helper import create_and_save_transform_image, create_and_save_transform_image3

n_feats = 512
transform_type = 'spectrogram'
ws = 10
spec_dir = 'D:/Documents/Thesis/Saved Transforms/Images/Spectrograms/' + str(ws) + '/' + str(n_feats) + '/'
wav_list = os.listdir(wav_dir)
transformer = Transform()

n_wavs = len(wav_list)
n_transformed = 0
failed_transforms = []
for wav_name in wav_list:
    try:
        signal, sr = librosa.load(wav_dir + wav_name)

        print('• Creating spectrogram of ' + wav_name)
        transform = transformer.calculate_transform(samples=signal,
                                                    sample_rate=sr,
                                                    n_feats=n_feats,
                                                    transform_type=transform_type,
                                                    window_size=ws)
        spec_name = wav_name.replace('.wav', '.png')
        create_and_save_transform_image3(spec_dir + spec_name, transform)
        n_transformed += 1
    except:
        failed_transforms.append(wav_name)
        continue
with open(spec_dir + 'Fails/fails.txt', 'w+') as f:
    for failed_transform in failed_transforms:
        f.write(failed_transform + '\n')
