from basic_classes.constants import wav_dir
import os
from basic_classes.transforms import Transform
import librosa
from .helper import load_transform
import numpy as np
import skimage

n_feats = 512
transform_type = 'spectrogram'
ws = 10
spec_dir = 'D:/Documents/Thesis/Saved Transforms/Images/Spectrograms/' + str(ws) + '/' + str(n_feats) + '/'
wav_list = os.listdir(wav_dir)
transformer = Transform()

wav_name = wav_list[0]
signal, sr = librosa.load(wav_dir + wav_name)

print('• Creating spectrogram of ' + wav_name)

transform = transformer.calculate_transform(samples=signal,
                                            sample_rate=sr,
                                            n_feats=n_feats,
                                            transform_type=transform_type,
                                            window_size=ws)


spec_name = wav_name.replace('.wav', '.png')

transform = skimage.util.img_as_ubyte(transform)
print(transform.shape)
print(np.amin(transform), np.amax(transform))
