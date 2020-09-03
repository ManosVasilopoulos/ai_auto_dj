import audioread
import contextlib
import os
import sys
import wave
from .constants_audio import mp3_dir2, wav_dir2


# This function converts an .mp3 file to .wav
# Input: Name of the file to be converted
# Output: New .wav file with the name of the original file saved in the same directory.

def decode(fname, mp3dir, wavdir):
    file_path = mp3dir + fname

    if not os.path.exists(file_path):
        print("File not found.", file=sys.stderr)
        sys.exit(1)

    with audioread.audio_open(file_path) as f:
        print('Input file: %i channels at %i Hz; %.1f seconds.' %
              (f.channels, f.samplerate, f.duration),
              file=sys.stderr)
        print('Backend:', str(type(f).__module__).split('.')[1],
              file=sys.stderr)
        fname = fname.replace('mp3', 'wav')
        fname = fname.replace('Mp3', 'wav')
        with contextlib.closing(wave.open(wavdir + fname, 'w')) as of:
            of.setnchannels(f.channels)
            of.setframerate(f.samplerate)
            of.setsampwidth(2)
            for buf in f:
                of.writeframes(buf)
    print('------------------------------------------------------')


##################################################################################

mp3_list = os.listdir(mp3_dir2)
n_tracks = len(mp3_list)
for i, filename in enumerate(mp3_list):
    print('Decoding: ' + filename)
    try:
        decode(filename, mp3_dir2, wav_dir2)
        print('Finished ' + str(i+1) + ' out of ' + str(n_tracks))
    except Exception as e:
        print('\n♦ ' + e + '\n')
        with open(wav_dir2 + 'failed.txt', 'a') as txt:
            txt.write(filename + '\n')
