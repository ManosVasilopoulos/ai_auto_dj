from player.equipment.deck_handler import DeckHandler
from player.midi.midi_handler import MidiHandler
from player.metadata.sql_handler import SQLHandler
import time

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')
deck_handler1 = DeckHandler(midi_handler.midiout, 1)
deck_handler2 = DeckHandler(midi_handler.midiout, 2)

# RESET BPM
input('Press enter to start testing "fast_forward".')
time.sleep(2)
deck_handler1.jump_to_start()
deck_handler1.fast_forward(1.3)

deck_handler2.jump_to_start()
deck_handler2.fast_forward(0.07)
