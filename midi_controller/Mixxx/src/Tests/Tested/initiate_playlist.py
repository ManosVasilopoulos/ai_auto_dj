"""
1) move song-focus at the top of playlist
2) load each track in order to be analyzed
"""
from midi_out_port import get_midi_port
from playlist import Mixx_DJ
import os
import numpy as np
import time

print('Counting 3 seconds to begin...')
time.sleep(3)

playlist_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\\Mixxx\\1'
dj = Mixx_DJ()

playlist = os.listdir(playlist_dir)

dj.go_to_top_on_playlist(np.array(playlist))
dj.load_all_tracks(np.array(playlist))
