import numpy as np
from scipy import signal
import librosa


class Transform:

    @staticmethod
    def __get_stft_real(rate, data, win_time, fft_size):
        # All wav files have a sample rate = 44100 Hz which means 44100 samples per second
        # Nx = 441 --> 10 ms of time
        # win_time-->window length in milliseconds
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # nfft is the input number divided by 2
        window_samples = int(win_time * one_ms)  # 10 * 44.1 = 441 ==> 10 milliseconds
        _, _, zxx = signal.stft(x=data, window=signal.get_window('hamming', Nx=window_samples), nperseg=window_samples,
                                noverlap=0, fs=rate, nfft=fft_size)

        pxx = np.real(zxx)
        print('Size of STFT: (' + str(f.size) + ',' + str(t.size) + ')')

        return pxx

    @staticmethod
    def __get_stft_imaginary(rate, data, win_time, fft_size):
        # All wav files have a sample rate = 44100 Hz which means 44100 samples per second
        # Nx = 441 --> 10 ms of time
        # win_time-->window length in milliseconds
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # nfft is the input number divided by 2
        window_samples = int(win_time * one_ms)  # 10 * 44.1 = 441 ==> 10 milliseconds
        _, _, zxx = signal.stft(x=data, window=signal.get_window('hamming', Nx=window_samples), nperseg=window_samples,
                                noverlap=0, fs=rate, nfft=fft_size)

        pxx = np.imag(zxx)

        return pxx

    @staticmethod
    def __get_real_im_stft(rate, data, win_time, fft_size):
        # All wav files have a sample rate = 44100 Hz which means 44100 samples per second
        # Nx = 441 --> 10 ms of time
        # win_time-->window length in milliseconds
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # nfft is the input number divided by 2
        window_samples = int(win_time * one_ms)  # 10 * 44.1 = 441 ==> 10 milliseconds
        f, t, zxx = signal.stft(x=data, window=signal.get_window('hamming', Nx=window_samples), nperseg=window_samples,
                                noverlap=0, fs=rate, nfft=fft_size)

        p_real = np.real(zxx)

        p_im = np.imag(zxx)

        return p_real, p_im

    @staticmethod
    def __get_spectrogram(rate, data, win_time, fft_size):
        # All wav files have a sample rate = 44100 Hz which means 44100 samples per second
        # Nx = 441 --> 10 ms of time
        # win_time-->window length in milliseconds
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # with hamming window use 0 noverlap--with hann use 50% of nperseg==window_samples
        window_samples = int(win_time * one_ms) * 2  # 10 * 44.1 * 2= 882 ==> 20 milliseconds
        window = signal.get_window('hann', Nx=window_samples)
        if win_time >= 50:
            fft_size = window_samples
        _, _, zxx = signal.stft(x=data, window=window, nperseg=window_samples,
                                noverlap=window_samples // 2, fs=rate, nfft=fft_size)

        # print('• Shape of Spectrogram: (' + str(f.size) + ',' + str(t.size) + ')')

        spectrogram = np.absolute(zxx) ** 2
        return librosa.power_to_db(spectrogram)

    @staticmethod
    def __get_melspectrogram(rate, data, win_time, n_mels):
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        fft_size = 2048
        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # nfft is the input number divided by 2

        # with hamming window use 0 noverlap--with hann use 50% of nperseg==window_samples
        window_samples = int(win_time * one_ms) * 2  # 10 * 44.1 * 2= 882 ==> 20 milliseconds
        window = signal.get_window('hann', Nx=window_samples)
        if win_time >= 50:
            fft_size = window_samples
        _, _, zxx = signal.stft(x=data, window=window, nperseg=window_samples,
                                noverlap=window_samples // 2, fs=rate, nfft=fft_size)

        spectrogram = np.absolute(zxx) ** 2
        pxx = librosa.feature.melspectrogram(
            S=spectrogram,
            n_mels=n_mels
        )

        """WORST"""
        # return librosa.power_to_db(pxx**2)
        """BETTER"""
        # return 20 * np.log10(pxx + 1e-07)
        """BEST"""
        return librosa.power_to_db(pxx)

    @staticmethod
    def __get_constant_q(rate, data, n_cqt=84):
        cqt = librosa.core.cqt(data, sr=rate, hop_length=512, n_bins=n_cqt, bins_per_octave=12, window='hann')
        return librosa.amplitude_to_db(np.abs(cqt))

    def __get_mfcc(self, rate, data, win_time, n_mfcc):
        melspectrogram = self.__get_melspectrogram(rate, data, win_time, 256)
        mfcc = librosa.feature.mfcc(S=melspectrogram, sr=rate, n_mfcc=n_mfcc)
        return mfcc

    def calculate_transform(self, samples, sample_rate, transform_type, n_feats, window_size,
                            print_transform_shapes=False):

        if transform_type == 'spectrogram':
            x = self.__get_spectrogram(rate=sample_rate, data=samples, win_time=window_size, fft_size=n_feats)
        elif transform_type == 'melspectrogram':
            x = self.__get_melspectrogram(rate=sample_rate, data=samples, win_time=window_size, n_mels=n_feats)
        elif transform_type == 'stft_real':
            x = self.__get_stft_real(rate=sample_rate, data=samples, win_time=window_size, fft_size=n_feats)
        elif transform_type == 'stft_imaginary':
            x = self.__get_stft_imaginary(rate=sample_rate, data=samples, win_time=window_size, fft_size=n_feats)
        elif transform_type == 'mfcc':
            x = self.__get_mfcc(rate=sample_rate, data=samples, win_time=window_size, n_mfcc=n_feats)
        elif transform_type == 'cqt':
            if n_feats > 256:
                raise Exception('TransformError: Constant-Q transform requires a number of bins lower than 256.'
                                '\nGiven value: ' + str(n_feats))
            x = self.__get_constant_q(rate=sample_rate, data=samples, n_cqt=n_feats)
        else:
            x_real, x_im = self.__get_real_im_stft(rate=sample_rate, data=samples, win_time=window_size,
                                                   fft_size=n_feats)
            x = [x_real, x_im]

        if print_transform_shapes:
            print("• Shape of '" + transform_type + "': " + str(x.shape))
        return x

    @staticmethod
    def get_bad_spectrogram(data, rate, fft_size, win_time):
        # All wav files have a sample rate = 44100 Hz which means 44100 samples per second
        # Nx = 441 --> 10 ms of time
        # win_time-->window length in milliseconds
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # with hamming window use 0 noverlap--with hann use 50% of nperseg==window_samples
        window_samples = int(win_time * one_ms)  # 10 * 44.1 = 441 ==> 10 milliseconds
        window = signal.get_window('hamming', Nx=window_samples)
        _, _, zxx = signal.stft(x=data, window=window, nperseg=window_samples,
                                noverlap=0, fs=rate, nfft=fft_size)

        # print('• Shape of Spectrogram: (' + str(f.size) + ',' + str(t.size) + ')')

        spectrogram = np.absolute(zxx) ** 2
        return librosa.power_to_db(spectrogram)

    @staticmethod
    def get_good_spectrogram(data, rate, fft_size, win_time):
        # All wav files have a sample rate = 44100 Hz which means 44100 samples per second
        # Nx = 441 --> 10 ms of time
        # win_time-->window length in milliseconds
        one_ms = rate / 1000  # rate=44100 cycles per second. Which means 44.1 cycles per millisecond ==> one ms is represented as 44.1

        # we do this because of the way signal.stft is calculated.
        fft_size *= 2
        fft_size -= 2
        # with hamming window use 0 noverlap--with hann use 50% of nperseg==window_samples
        window_samples = int(win_time * one_ms) * 2  # 10 * 44.1 = 441 ==> 10 milliseconds
        window = signal.get_window('hann', Nx=window_samples)
        if win_time >= 50:
            fft_size = window_samples
        _, _, zxx = signal.stft(x=data, window=window, nperseg=window_samples,
                                noverlap=window_samples // 2, fs=rate, nfft=fft_size)
        # print('• Shape of Spectrogram: (' + str(f.size) + ',' + str(t.size) + ')')

        spectrogram = np.absolute(zxx) ** 2
        return librosa.power_to_db(spectrogram)
