import librosa
import librosa.display
from .constants_visuals import wav_dir, wav_dir2
import matplotlib.pyplot as plt
import numpy as np

def main():

    song_name = '04 - Thriller.wav'
    sample_path = wav_dir + song_name

    signal, sr = librosa.load(sample_path, sr=8000, mono=True)
    max_1 = np.amax(signal)
    if np.abs(np.amin(signal)) > max_1:
        max_1 = np.abs(np.amin(signal))

    signal = signal / max_1
    plt.figure()
    librosa.display.waveplot(signal, sr)
    plt.title('Thriller by Michael Jackson - Waveform')
    plt.show()
if __name__ == '__main__':
    main()