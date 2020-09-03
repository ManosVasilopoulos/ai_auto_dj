import os, time
from rekordbox_util import RekordboxHandler
from helper import get_playlist_points, get_bpm_of_tracks
from constants import playlist_path, delay_constant

dj = RekordboxHandler()
dj.open_port()

print('Sleeping for 5 seconds...')
time.sleep(5)

temp = os.listdir(playlist_path)
tracks = []
for t in temp:
    if 'mp3' in t:
        tracks.append(t)
track_counter = 0
number_of_tracks = len(tracks)
if number_of_tracks == 0:
    raise Exception('NO SONGS FOUND.')

# all points is an array
_, all_points = get_playlist_points()
bpm_of_all = get_bpm_of_tracks()
print(all_points)
time.sleep(0.5)

points_1 = all_points[track_counter]
bpm_1 = bpm_of_all[track_counter]
points_2 = all_points[track_counter + 1]
bpm_2 = bpm_of_all[track_counter + 1]

################################################
# INITIALIZATIONS
dj.master_tempo(1)
dj.master_tempo(2)
dj.fader_down(1)
dj.fader_down(2)

################################################
# First Tracks

# Deck-1
dj.browse_to_next()
dj.load_track_on_deck(1)
time.sleep(1)
print('Loaded Track on Deck 1')
dj.jump_to_track_start(1)
cue_point_1 = points_1[0]
dj.set_cue(1, cue_point_1)
dj.press_cue(1)
time.sleep(1)
print('Set cue on Deck 1')

dj.fader_up(1)
print('Fader 1 UP')

mix_point_1 = points_1[2]
delay = dj.press_play(1)
print('Pressed Play on Deck 1')
# press_play_with_style(1)

track_counter += 1

next_deck = 2
prev_deck = 1
mix_point_prev = mix_point_1
stop_mix_point_prev = points_1[3]
cue_point_prev = cue_point_1
bpm_prev = bpm_1
points_prev = points_1

############################################
# Repeat this till the end of the playlist
while track_counter < number_of_tracks:
    # Deck-To Play
    points_next = all_points[track_counter]
    bpm_next = bpm_of_all[track_counter]

    # Browse, Load, Jump to Start
    delay += dj.browse_to_next()
    delay += dj.load_track_on_deck(next_deck)
    delay += dj.jump_to_track_start(next_deck)

    cue_point_next = points_next[0]

    # Set Cue, Press Cue
    delay += dj.set_cue(next_deck, cue_point_next)
    delay += dj.press_cue(next_deck)

    if track_counter == 1:
        time.sleep(mix_point_prev - cue_point_prev - delay)
    else:
        time.sleep((mix_point_prev - cue_point_prev)*(bpm_next/bpm_prev) - delay)

    delay = dj.press_play(next_deck)
    delay += dj.fader_up_and_sync(next_deck)
    print('Fader' + str(next_deck) + 'Up and Pressed Sync')
    mix_point_next = points_next[3]

    track_counter += 1

    # Deck-Playing
    mix_point_prev = points_prev[2]
    stop_mix_point_prev = points_prev[3]

    time.sleep(stop_mix_point_prev - mix_point_prev - 0.5 - delay)

    # Fader Down, Press Cue (To Stop)
    delay = dj.fader_down(prev_deck)
    print('Fader ' + str(prev_deck) + ' Down')
    delay += dj.press_cue(prev_deck)
    delay += dj.press_sync(prev_deck)

    if next_deck == 1:
        next_deck = 2
        prev_deck = 1
    else:
        next_deck = 1
        prev_deck = 2

    points_prev = points_next
    mix_point_prev = points_prev[2]
    stop_mix_point_prev = points_prev[3]
    bpm_prev = bpm_next
    # One Browse to highlight on playlist and then one more on the beginning of loop to move to next
    delay += dj.browse_to_next()

print('Finished Mix.')
dj.close_port()
