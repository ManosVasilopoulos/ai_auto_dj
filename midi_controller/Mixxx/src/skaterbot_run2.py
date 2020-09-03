from player.player import Mixx_DJ
from player.metadata.metadata_handler import MetaDataHandler
import sys
from time import sleep
from numpy import roll as nproll

playlist_name = sys.argv[1]

metadata_handler = MetaDataHandler(playlist_name)
playlist_db = metadata_handler.get_tracks_full_metadata()
playlist_db = metadata_handler.sort_metadata_by_bpm(playlist_db)

playlist_tracks_names_sorted = [x[0] for x in playlist_db]
print('The tracks that will be mixed are presented below in a given order.')
for i, track_name in enumerate(playlist_tracks_names_sorted):
    print('Track:', i, track_name)

dj = Mixx_DJ()

current_side = 1
next_side = 2

try:
    # Initializing DJ Setup
    dj.setups.setup_deck(1)
    dj.setups.setup_deck(2)
    dj.setups.setup_mixer()

    # Go at the top of playlist
    dj.pressings.scroll_up(playlist_db.shape[0], see_scrolling=True)

    # Setup the first song on the first deck
    dj.get_next_song_ready(current_side, playlist_db[0])

    # Move Fader of the second channel down
    dj.moves.move_fader_down(next_side)
    print('Moved Fader -', next_side, 'down.')
    sleep(2)

    cue_point1 = playlist_db[0, 1][0]
    mix_point1 = playlist_db[0, 1][2]

    # Move down by one song on library panel
    dj.pressings.scroll_down(1)  # prepare for next song

    # Setup the second song on the second deck
    dj.get_next_song_ready(2, playlist_db[1])

    # Move the playlist by two songs - Roll is used in order to have the correct number of loops
    playlist_db = nproll(a=playlist_db, shift=-2, axis=0)
    print(playlist_db)

    # Press the 'Play'-button of the first deck
    dj.pressings.press_play(current_side)

    print('sleeping for:', mix_point1 - cue_point1)
    sleep(mix_point1 - cue_point1)

    for track in playlist_db:
        latency = dj.pressings.press_play(next_side)
        print('Pressed play (deck-' + str(next_side) + ')')

        latency += dj.moves.move_fader_up(next_side)
        print('Fader Up (channel-' + str(next_side) + ')')
        latency += dj.pressings.press_beat_sync(next_side)
        print('Pressed beat_sync (deck-' + str(next_side) + ')')

        latency = dj.wait_for_mix(current_side, latency)
        latency += dj.moves.move_fader_down(current_side)
        print('Fader Up (channel-' + str(current_side) + ')')
        latency += dj.pressings.press_cue(current_side)
        print('Pressed cue (deck-' + str(current_side) + ')')

        latency += dj.pressings.reset_bpm(next_side)
        print('Pressed reset_bpm (deck-' + str(next_side) + ')')

        to_mix_time = dj.get_tomix_time(current_side, next_side) - latency

        latency = dj.pressings.scroll_down(1)
        print('Scrolled Down')

        current_side, next_side = dj.swap_sides(current_side)
        latency += dj.get_next_song_ready(next_side, track)

        to_mix_time -= latency
        print('Sleeping for', to_mix_time)
        sleep(to_mix_time)
except Exception as e:
    print(e)
except KeyboardInterrupt:
    print('Process Interrupted.')
# 4 - Shut Down Everything
try:
    dj.setups.setup_deck(1)
    dj.setups.setup_deck(2)
    dj.midi_handler.close_all_ports()
    print('CLOSED ALL MIDI-PORTS')
except:
    pass
print('FINISHED MIXING...')
