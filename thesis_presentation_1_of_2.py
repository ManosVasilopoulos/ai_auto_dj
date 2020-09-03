from poi_detector.src.predict.predict_pois_of_playlist import predict_poi_and_save_in_csv
from midi_controller.Mixxx.src.skaterbot_performance import dj_perform
from sys import argv as sys_argv
from pandas import DataFrame

playlist_name = sys_argv[1]

print('Analyzing playlist...\n')
(relative_poi_csv, relative_poi), (precise_poi_csv, precice_poi) = predict_poi_and_save_in_csv(playlist_name)

