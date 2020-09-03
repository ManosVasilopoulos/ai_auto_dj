from player.equipment.deck_handler import DeckHandler
from player.midi.midi_handler import MidiHandler
from player.metadata.sql_handler import SQLHandler
import time

track_name = '09 Goosebumps (feat. Kendrick Lamar)'
sql_handler = SQLHandler()
track_id = sql_handler.get_track_id(track_name)

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')
deck_handler1 = DeckHandler(midi_handler.midiout, 1)
deck_handler2 = DeckHandler(midi_handler.midiout, 2)

# RESET BPM
input('Press enter to start testing "strip_search".')
time.sleep(2)
deck_handler1.strip_search()
deck_handler1.strip_search()
deck_handler2.strip_search()
deck_handler2.strip_search()
