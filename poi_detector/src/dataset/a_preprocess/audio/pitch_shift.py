import librosa
import os
from soundfile import write as sfwrite
from .constants_audio import wav_dir, pitch_shifted_dir

# This function converts an .mp3 file to .wav
# Input: Name of the file to be converted
# Output: New .wav file with the name of the original file saved in the same directory.
##################################################################################

wav_dir_main = wav_dir

wav_list = os.listdir(wav_dir_main)
#semitones_list = [6.0, 3.0, -3.0, -6.0]
semitones_list = [6.0, -6.0]
n_wavs = len(wav_list)
skipped = []
for semitones in semitones_list:
    for i, filename in enumerate(wav_list):
        if '.wav' in filename:
            path = wav_dir_main + filename
            try:
                samples, sr = librosa.load(path, mono=True, sr=44100)
            except Exception as e:
                print('\n♦ ' + e + '\n')
                with open(pitch_shifted_dir + 'failed.txt', 'a') as txt:
                    txt.write(filename + '\n')
                skipped.append(filename)
                continue
            print('Pitching...')
            print(samples.shape)
            pitched_samples = librosa.effects.pitch_shift(samples, sr=sr, n_steps=semitones)
            print(pitched_samples.shape)
            if semitones == 3.0:
                dir_p = pitch_shifted_dir + '+3/'
            elif semitones == -3.0:
                dir_p = pitch_shifted_dir + '-3/'
            elif semitones == 6.0:
                dir_p = pitch_shifted_dir + '+6/'
            elif semitones == -6.0:
                dir_p = pitch_shifted_dir + '-6/'
            else:
                raise Exception('WRONG SEMITONES')
            print('Writing: ' + filename)
            pitched_path = dir_p + filename.replace('.wav', '-pitch-' + str(int(semitones)) + '.wav')
            sfwrite(pitched_path, pitched_samples, samplerate=sr)
            print('Finished pitch-shift with ' + str(semitones))
            print(str(i) + ' out of ' + str(n_wavs))

print('-----------------------------------------------')
print('Skipped: ')
for sk in skipped:
    print(sk)
