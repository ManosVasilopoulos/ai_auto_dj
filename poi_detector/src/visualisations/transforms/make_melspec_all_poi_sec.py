"""
    while being in __main__ directory run 'py -m visualisations.make_spectrogram'
"""

from .constants_visuals import wav_dir, visuals_dir
import librosa
from basic_classes.transforms import Transform
import matplotlib.pyplot as plt
import numpy as np
import librosa.display


def calculate_column():
    pois = [21.267,
            37.462,
            90.225,
            106.425,
            146.921,
            163.124,
            217.741,
            233.933,
            237.969,
            254.156,
            318.846,
            343.120]

    # one column represents 10ms ==> 0.073 is column 7

    pois_indexes = [
                    [2127],
                    [3746],
                    [9023],
                    [10643],
                    [14692],
                    [16312],
                    [21774],
                    [23393],
                    [23797],
                    [25416],
                    [31885],
                    [34312]
                    ]
    return pois_indexes


def main():
    song_name = '04 - Thriller.wav'
    sample_path = wav_dir + song_name
    transformer = Transform()

    signal, sr = librosa.load(sample_path, sr=44100, mono=True)

    z = transformer.calculate_transform(signal, sr, 'melspectrogram', 1024)
    z = np.transpose(z)

    z[:, 2127:2177] = -9
    z[:, 3746:3786] = -9
    z[:, 9023:9073] = -9
    z[:, 10643:10683] = -9
    z[:, 14692:14742] = -9
    z[:, 16312:16362] = -9
    z[:, 21774:21824] = -9
    z[:, 23393:23443] = -9
    z[:, 23797:23847] = -9
    z[:, 25416:25456] = -9
    z[:, 31885:31935] = -9
    z[:, 34312:34362] = -9

    """
    x = np.arange(0, 357.65, 0.01)
    y = np.arange(0, 44100, 44100 / 1024)
    x, y = np.meshgrid(x, y)
    plt.subplot()
    plt.pcolor(x, y, z, cmap='viridis', vmin=-100, vmax=-9)

    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.colorbar()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency (Hz)')
    """
    librosa.display.specshow(z, cmap='viridis', x_axis='time', y_axis='mel', sr=sr, fmax=sr//2)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Thriller by Michael Jackson - Mel-Spectrogram with all Points of Interest')
    plt.show()

if __name__ == '__main__':
    main()
