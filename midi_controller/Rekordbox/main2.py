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
# STEP 0
# First Moves When Loading Program
dj.master_tempo(1)
dj.master_tempo(2)
dj.fader_down(1)
dj.fader_down(2)

################################################
# Step 1
dj.browse_to_next()
dj.load_track_on_deck(1)
dj.browse_to_next()
dj.load_track_on_deck(2)

################################################
# Step 2
dj.fader_up(1)

################################################
# Step 3
points_1 = all_points[track_counter]
bpm_1 = bpm_of_all[track_counter]
# After reading points increment counter
track_counter += 1

""" Points of track on Deck 1 """
cue_point_1 = points_1[0]
stop_intro_point_1 = points_1[1]
mix_point_1 = points_1[2]
stop_mix_point_1 = points_1[3]

points_2 = all_points[track_counter]
bpm_2 = bpm_of_all[track_counter]
# After reading points increment counter
track_counter += 1

""" Points of track on Deck 2 """
cue_point_2 = points_2[0]
stop_intro_point_2 = points_2[1]
mix_point_2 = points_2[2]
stop_mix_point_2 = points_2[3]

##############################################
# Step 4
dj.jump_to_track_start(1)
dj.set_cue(1, cue_point_1)

##############################################
# Step 5
prev_deck = 1
next_deck = 2
prev_points = points_1
next_points = points_2
cue_prev = prev_points[0]
cue_next = next_points[0]
mix_prev = prev_points[2]
mix_next = next_points[2]
stop_mix_prev = prev_points[3]
stop_mix_next = next_points[3]
mix_duration_prev = 0
delay = 0
""" Don't get confused by these below"""
bpm_prev = bpm_1
bpm_prev2 = bpm_1

##############################################
# Step 6
dj.press_play(1)


####################################################


while track_counter <= number_of_tracks:
    # Alpha
    delay += dj.set_cue(next_deck, cue_next)
    delay += dj.press_sync(next_deck)
    # Beta
    time.sleep(mix_prev - (cue_prev + mix_duration_prev*(bpm_prev2/bpm_prev)) - delay)
    delay = 0
    # Gamma
    delay += dj.press_play(next_deck)
    # Delta
    delay += dj.fader_up(next_deck)
    delay += dj.press_sync(next_deck)
    # Epsilon
    print('DELAY for mix: ' + str(delay))
    time.sleep(stop_mix_prev - mix_prev - delay - 1)
    mix_duration_prev = stop_mix_prev - mix_prev - delay
    delay = 0
    # Zeta
    delay += dj.fader_down(prev_deck)
    delay += dj.tempo_reset(next_deck)
    # Eta
    delay += dj.press_cue(prev_deck)
    # Theta
    prev_points = next_points
    bpm_prev2 = bpm_of_all[track_counter - 2]
    try:
        next_points = all_points[track_counter]
        cue_next = next_points[0]
    except:
        print('No more Tracks in playlist.')
        break
    bpm_prev = bpm_of_all[track_counter - 1]

    track_counter += 1


    if next_deck == 1:
        prev_deck = 1
        next_deck = 2
    else:
        prev_deck = 2
        next_deck = 1

    stop_mix_prev = prev_points[3]
    mix_prev = prev_points[2]
    # One Browse to highlight on playlist and then one more on the beginning of loop to move to next
    delay += dj.browse_to_next()
    delay += dj.browse_to_next()
    delay += dj.load_track_on_deck(next_deck)
    delay += dj.jump_to_track_start(next_deck)

print('Finished Mix.')


dj.master_tempo(1)
dj.master_tempo(2)
dj.close_port()
