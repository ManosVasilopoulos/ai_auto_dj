"""
A class that handles audio and outputs a transform.
This class should provide a method that handles the whole process:
    1) MP3 to WAV
    2) WAV to Transform
    3) Reshape of Transform
"""
from poi_detector.src.dataset.a_preprocess.audio.decoder import MP3decoder
from os import listdir as os_listdir
from os.path import join as os_path_join

from poi_detector.src.predict.helper import keep_files
from poi_detector.src.predict.helper import create_sub_dir
from poi_detector.src.predict.helper import move_file


def decode_playlist(playlist_dir):
    mp3_decoder = MP3decoder()

    mp3_playlist = keep_files(os_listdir(playlist_dir), 'mp3')
    if len(mp3_playlist) == 0:
        return []
    mp3_dir = create_sub_dir(playlist_dir, 'mp3_folder')

    print(mp3_playlist)
    wav_playlist = []
    for mp3_file in mp3_playlist:
        # Decode MP3-file --> Create corresponding WAV-file
        wav_filename = mp3_decoder.decode(mp3_file, playlist_dir, playlist_dir)
        wav_playlist.append(wav_filename)

        # Move MP3-file from its current directory to a subdirectory "/mp3"
        from_path = os_path_join(playlist_dir, mp3_file)
        to_path = os_path_join(mp3_dir, mp3_file)
        move_file(from_path, to_path)

    return wav_playlist
