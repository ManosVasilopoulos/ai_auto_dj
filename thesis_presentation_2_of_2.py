from midi_controller.Mixxx.src.skaterbot_performance import dj_perform
from sys import argv as sys_argv
from os.path import join as os_path_join

playlist_name = sys_argv[1]

playlist_dir = 'D:/Documents/Thesis/Project Skaterbot/Playlists/Mixxx/'
relative_poi_csv = 'pois_locator_v2.csv'
csv_path = os_path_join(playlist_dir, playlist_name, relative_poi_csv)

print('DJ Performance...\n')
dj_perform(playlist_name, relative_poi_csv)
