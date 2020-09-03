import os, time
from rekordbox_util import RekordboxHandler
from helper import get_playlist_points, get_bpm_of_tracks
from constants import playlist_path

dj = RekordboxHandler()
dj.open_port()

print('Sleeping for 2 seconds...')
time.sleep(2)

temp = os.listdir(playlist_path)
tracks = []
for t in temp:
    if 'wav' in t:
        tracks.append(t)
track_counter = 0
number_of_tracks = len(tracks)
if number_of_tracks == 0:
    raise Exception('NO SONGS FOUND.')

# all points is an array
_, all_points = get_playlist_points()
_, bpm_of_all = get_bpm_of_tracks()

print(all_points)
print(bpm_of_all)

################################################
# Step 3
points_1 = all_points[track_counter]
points_2 = all_points[track_counter + 1]
""" Points of track on Deck 1 """
cue_point_1 = points_1[0]
cue_point_2 = points_2[0]
##############################################
# Step 4
dj.jump_to_track_start(1)
time.sleep(1)
dj.set_cue(1, cue_point_1)
time.sleep(1)

# Step 4
dj.jump_to_track_start(2)
time.sleep(1)
dj.set_cue(2, cue_point_2)
time.sleep(2)

dj.close_port()