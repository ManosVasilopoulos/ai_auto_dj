import librosa
import os
from soundfile import write as sfwrite
from .constants_audio import wav_dir, time_stretched_dir

# This function converts an .mp3 file to .wav
# Input: Name of the file to be converted
# Output: New .wav file with the name of the original file saved in the same directory.
##################################################################################

wav_dir_main = wav_dir

wav_list = os.listdir(wav_dir_main)
stretches_list = [1.25, 0.75]
n_wavs = len(wav_list)
skipped = []
for stretch in stretches_list:
    for i, filename in enumerate(wav_list):
        if '.wav' in filename:
            path = wav_dir_main + filename
            try:
                samples, sr = librosa.load(path, mono=True, sr=44100)
            except Exception as e:
                print('\n♦ ' + e + '\n')
                with open(time_stretched_dir + 'failed.txt', 'a') as txt:
                    txt.write(filename + '\n')
                skipped.append(filename)
                continue
            print('Stretching: ' + filename)
            print('Samples before: ' + str(samples.shape))
            stretched_samples = librosa.effects.time_stretch(samples, rate=stretch)
            print('Samples after: ' + str(stretched_samples.shape))
            if stretch == 1.25:
                dir_p = time_stretched_dir + '+25%/'
            elif stretch == 0.75:
                dir_p = time_stretched_dir + '-25%/'
            else:
                raise Exception('WRONG SEMITONES')
            stretched_path = dir_p + filename.replace('.wav', '-stretch' + str(stretch) + '.wav')
            sfwrite(stretched_path, stretched_samples, samplerate=sr)
            print('Finished time-stretch with ' + str(stretch))
            print(str(i+1) + ' out of ' + str(n_wavs))
        print('-----------------------------------------------')


print('Skipped: ')
for sk in skipped:
    print(sk)
