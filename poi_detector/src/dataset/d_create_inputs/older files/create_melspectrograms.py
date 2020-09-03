from basic_classes.constants import wav_dir
import os
from basic_classes.transforms import Transform
import librosa
from .helper import create_and_save_transform_image

n_feats = 512
transform_type = 'melspectrogram'
ws = 10
mel_spec_dir = 'D:/Documents/Thesis/Saved Transforms/Images/Melspectrograms/' + str(ws) + '/' + str(n_feats) + '/'
wav_list = os.listdir(wav_dir)
transformer = Transform()

for wav_name in wav_list:
    signal, sr = librosa.load(wav_dir + wav_name)

    print('• Creating melspectrogram of ' + wav_name)
    transform = transformer.calculate_transform(samples=signal,
                                                sample_rate=sr,
                                                n_feats=n_feats,
                                                transform_type=transform_type,
                                                window_size=ws)
    create_and_save_transform_image(mel_spec_dir + wav_name, transform)
