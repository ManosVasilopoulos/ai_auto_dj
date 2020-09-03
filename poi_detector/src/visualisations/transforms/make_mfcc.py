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
    song_name = '2 - The Box.wav'
    #song_name = '02 EARFQUAKE.wav'
    #song_name = 'JACKBOYS - OUT WEST.wav'
    sample_path = wav_dir2 + song_name
    transformer = Transform()

    signal, sr = librosa.load(sample_path, sr=44100, mono=True)

    x = transformer.calculate_transform(signal, sr, 'mfcc', 12)
    x = np.transpose(x)

    plt.figure(figsize=(7, 4))
    ax_img = librosa.display.specshow(x, cmap='viridis', x_axis='time', sr=sr)
    plt.colorbar()
    plt.title('The Box by Roddy Ricch - Mel-Frequency Cepstral Coefficients')
    #plt.title('EARFQUAKE by Tyler, The Creator - Mel-Frequency Cepstral Coefficients')
    #plt.title('OUT WEST by Jack Boys - Mel-Frequency Cepstral Coefficients')
    plt.show()


if __name__ == '__main__':
    main()
