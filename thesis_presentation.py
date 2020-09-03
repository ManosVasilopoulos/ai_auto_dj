from poi_detector.src.predict.predict_pois_of_playlist import predict_poi_and_save_in_csv
from midi_controller.Mixxx.src.skaterbot_performance import dj_perform
from sys import argv as sys_argv
from pandas import DataFrame

playlist_name = sys_argv[1]

print('Analyzing playlist...\n')
(relative_poi_csv, relative_poi), (precise_poi_csv, precice_poi) = predict_poi_and_save_in_csv(playlist_name)

print('DJ Performance...\n')
dj_perform(playlist_name, relative_poi_csv)


df_relative_poi = DataFrame(relative_poi)
print('Relative Points of Interest:\n', df_relative_poi)

df_precise_poi = DataFrame(precice_poi)
print('Precise Points of Interest:\n', df_precise_poi)
