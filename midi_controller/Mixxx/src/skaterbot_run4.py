from midi_controller.Mixxx.src.player.player import Mixx_DJ
from midi_controller.Mixxx.src.player.metadata.metadata_handler import MetaDataHandler
import sys
from time import sleep
from time import time

def dj_perform():
    playlist_name = sys.argv[1]
    poi_file = sys.argv[2]

    metadata_handler = MetaDataHandler(playlist_name, poi_file)
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
        dj.pressings.scroll_down(1)
        # Go at the top of playlist
        dj.pressings.scroll_up(playlist_db.shape[0], see_scrolling=True)

        # Move Fader of the second channel down
        dj.moves.move_fader_up(current_side)
        print('Moved Fader -', current_side, 'up.')
        dj.moves.move_fader_down(next_side)
        print('Moved Fader -', next_side, 'down.')
        sleep(2)

        latency = 0
        mix_current = 0
        pitch_perc = 0
        previous_mix_duration = 0
        previous_pitch_perc = 0
        for i, track in enumerate(playlist_db):
            start_time = time()
            # Load Track - Set Cue Point - Sync BPM
            dj.get_next_song_ready(next_side, track)

            if i == 0:
                waiting_time = 0
            else:
                if i == 1:
                    waiting_time = dj.get_tomix_time(current_side)
                else:
                    waiting_time = dj.get_tomix_time_modified(current_side, previous_mix_duration,
                                                              previous_pitch_perc)

                # Wait for current track to reach its mix point
                latency += time() - start_time
                print('Song:' + str(i), 'Waiting to reach mix-point in', waiting_time - latency, 'seconds!!')
                sleep(waiting_time - latency)
                print('\nReached Mix Point of current side. Start')

            """"""
            start_time = time()

            dj.pressings.press_play(next_side)
            print('\nPressed Play on next side.')

            dj.pressings.press_beat_sync(next_side)
            print('\nPressed BeatSync on next side.')
            dj.moves.move_fader_up(next_side)
            print('\nMoved fader up on next side.')

            if i > 0:
                elapsed_time = time() - start_time
                mix_current, pitch_perc = dj.mix_two_songs(current_side, next_side, elapsed_time)
                start_time = time()
            """"""

            """"""
            dj.moves.move_fader_down(current_side)

            dj.pressings.reset_bpm(next_side)

            dj.pressings.press_cue(current_side)

            print('\nFinished Mixing...')

            dj.focus_on_library()
            # Scroll Down by one position in library
            dj.pressings.scroll_down(1)
            current_side, next_side = dj.swap_sides(current_side)

            previous_mix_duration, previous_pitch_perc = mix_current, pitch_perc

            latency = time() - start_time
            """"""
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

if __name__ == '__main__':
    dj_perform()