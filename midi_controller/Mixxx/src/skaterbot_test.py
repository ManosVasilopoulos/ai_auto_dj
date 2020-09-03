from player.player import Mixx_DJ
from player.metadata.metadata_handler import MetaDataHandler
import sys
from time import sleep
from time import time
from numpy import roll as nproll

playlist_name = sys.argv[1]

metadata_handler = MetaDataHandler(playlist_name)
playlist_db = metadata_handler.get_tracks_full_metadata()
playlist_db = metadata_handler.sort_metadata_by_bpm(playlist_db)

playlist_tracks_names_sorted = [x[0] for x in playlist_db]

dj = Mixx_DJ()

current_side = 1
next_side = 2
sleep(3)
try:
    # Initializing DJ Setup
    print('--------------------SETUP DECK 1--------------------')
    dj.setups.setup_deck(1)
    print('--------------------SETUP DECK 2--------------------')
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
