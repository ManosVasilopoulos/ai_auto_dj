"""
    while being in __main__ directory run 'py -m visualisations.make_spectrogram'
"""

from .constants_visuals import wav_dir2, visuals_dir
import librosa
from basic_classes.transforms import Transform
import matplotlib.pyplot as plt
import numpy as np
import librosa.display

def main():
    #song_name = '2 - The Box.wav'
    song_name = '02 EARFQUAKE.wav'
    song_name = 'JACKBOYS - OUT WEST.wav'
    sample_path = wav_dir2 + song_name
    transformer = Transform()

    signal, sr = librosa.load(sample_path, sr=44100, mono=True)

    x = transformer.calculate_transform(signal, sr, 'cqt', 84)
    x = np.transpose(x)


    plt.figure(figsize=(7, 4))
    #librosa.display.specshow(x[:, 861: 3364], cmap='viridis', x_axis='time', y_axis='cqt_note', sr=39785)
    librosa.display.specshow(x[:, :1292], cmap='viridis', x_axis='time', y_axis='cqt_note', sr=39785)
    plt.colorbar(format='%+2.0f dB')
    #plt.title('EARFQUAKE by Tyler, The Creator - Constant-Q')
    #plt.title('The Box by Roddy Ricch - Constant-Q')
    plt.title('OUT WEST by Jack Boys - Constant-Q')
    plt.show()

if __name__ == '__main__':
    main()
