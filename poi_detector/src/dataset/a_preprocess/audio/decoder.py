import audioread
from contextlib import closing as contextlib_closing
from os.path import join as ospathjoin
from os.path import exists as ospathexists
from sys import exit as sysexit
from sys import stderr as sysstderr
from wave import open as waveopen


class MP3decoder:

    def __change_extention(self, fname: str):
        fname = fname.replace('mp3', 'wav')
        fname = fname.replace('Mp3', 'wav')
        fname = fname.replace('mP3', 'wav')
        fname = fname.replace('MP3', 'wav')
        return fname

    def decode(self, fname: str, mp3_dir: str, save_dir: str):
        """
        :param fname: name of the mp3 file that will be converted
        :param mp3_dir: directory of the mp3 file
        :param save_dir: directory of the wav file to be saved
        :return:
        """
        file_path = ospathjoin(mp3_dir, fname)

        if not ospathexists(file_path):
            print("File not found.", file=sysstderr)
            sysexit(1)

        fname = self.__change_extention(fname)
        print('New-Filename:', fname)
        with audioread.audio_open(file_path) as f:
            print('Input file: %i channels at %i Hz; %.1f seconds.' %
                  (f.channels, f.samplerate, f.duration),
                  file=sysstderr)
            print('Backend:', str(type(f).__module__).split('.')[1],
                  file=sysstderr)

            with contextlib_closing(waveopen(ospathjoin(save_dir, fname), 'w')) as of:
                of.setnchannels(f.channels)
                of.setframerate(f.samplerate)
                of.setsampwidth(2)
                for buf in f:
                    of.writeframes(buf)
        return fname
