"""
    while being in __main__ directory run 'py -m visualisations.make_spectrogram'
"""

from .constants_visuals import wav_dir2, visuals_dir
import librosa
from basic_classes.transforms import Transform
import matplotlib.pyplot as plt
import numpy as np
import librosa.display


def calculate_column():
    pois = [0.073, 8.153, 16.356, 32.766, 49.177, 81.996, 98.407, 114.817, 147.637, 164.048, 180.465]

    # one column represents 10ms ==> 0.073 is column 7

    pois_indexes = [
                    [7],
                    [815],
                    [1636],
                    [3277],
                    [4918],
                    [8200],
                    [9841],
                    [11482],
                    [14764],
                    [16405],
                    [18047]
                    ]
    return pois_indexes


def main():
    song_name = '2 - The Box.wav'
    sample_path = wav_dir2 + song_name
    transformer = Transform()

    signal, sr = librosa.load(sample_path, sr=44100, mono=True)

    x = transformer.calculate_transform(signal, sr, 'melspectrogram', 1024)
    x = np.transpose(x)

    x[:, 1636:1639] = 0
    """
    x[:, 7:57] = 0
    x[:, 815:865] = 0
    x[:, 3277:3327] = 0
    x[:, 4918:4968] = 0
    x[:, 8200:8250] = 0
    x[:, 9841:9891] = 0
    x[:, 11482:11532] = 0
    x[:, 14764:14814] = 0
    x[:, 16405:16455] = 0
    x[:, 18047:18097] = 0
    """

    plt.figure(figsize=(7, 4))
    # ax_img = plt.imshow(x[:, :3000], origin='lower')
    # plt.savefig(visuals_dir + song_name.replace('.wav', '.png'))
    ax_img = librosa.display.specshow(x[:, 1500:2000], cmap='viridis', x_axis='time', y_axis='mel', sr=sr, fmax=sr//2)
    plt.colorbar(format='%+2.0f dB')
    plt.title('The Box by Roddy Ricch - Mel-spectrogram with a Point of Interest')
    plt.show()


if __name__ == '__main__':
    main()
