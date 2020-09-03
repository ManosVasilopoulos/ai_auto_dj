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
sleep(3)
try:
    # Initializing DJ Setup
    dj.setups.setup_deck(1)
    dj.setups.setup_deck(2)

    # Focus on library's panel
    dj.focus_on_library()
    dj.pressings.scroll_down(1, True)
    # Go at the top of playlist
    dj.pressings.scroll_up(playlist_db.shape[0], see_scrolling=True)

    # Move Fader of the second channel down
    dj.moves.move_fader_up(current_side)
    print('Moved Fader -', next_side, 'down.')
    dj.moves.move_fader_down(next_side)
    print('Moved Fader -', next_side, 'down.')
    sleep(2)

    latency = 0
    for i, track in enumerate(playlist_db):
        # Load Track - Set Cue Point - Sync BPM
        latency += dj.get_next_song_ready(next_side, track)

        if i == 0:
            waiting_time = 0
        elif i == 1:
            waiting_time = dj.get_tomix_time(current_side) - latency
        else:
            waiting_time = dj.get_tomix_time_modified(current_side, next_side) - latency

        # Wait for current track to reach its mix point
        sleep(waiting_time)
        print('Reached Mix Point of current side. Start')
        latency = dj.pressings.press_play(next_side)
        print('Pressed Play on next side.')
        latency += dj.pressings.press_beat_sync(next_side)
        print('Pressed BeatSync on next side.')
        latency += dj.moves.move_fader_up(next_side)
        print('Moved fader up on next side.')

        if i == 0:
            waiting_time = 0
        else:
            # -0.5 is an arbitrary constant
            waiting_time = dj.get_end_of_mix_time(current_side) - latency - 0.5

        sleep(waiting_time)

        latency = dj.moves.move_fader_down(current_side)

        latency += dj.pressings.reset_bpm(next_side)

        latency += dj.pressings.press_cue(current_side)

        print('Finished Mixing...')

        latency += dj.focus_on_library()
        # Scroll Down by one position in library
        latency += dj.pressings.scroll_down(1)
        current_side, next_side = dj.swap_sides(current_side)

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
