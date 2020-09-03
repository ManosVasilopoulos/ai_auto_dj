from midi_controller.Mixxx.src.player.midi.midi_handler import MidiHandler
from midi_controller.Mixxx.src.player.midi.mappings import library_buttons, dj_buttons
import sys

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

button_name = sys.argv[1]

button_deck_1_note_on = dj_buttons[button_name]['deck_1']['note_on']
button_deck_1_note_off = dj_buttons[button_name]['deck_1']['note_off']
button_deck_2_note_on = dj_buttons[button_name]['deck_2']['note_on']
button_deck_2_note_off = dj_buttons[button_name]['deck_2']['note_off']

input('Press Enter to start configuring button "' + button_name + '"-deck-1 NOTE ON.\nPLEASE SETUP MIXXX LEARNING PROCESS')
midi_handler.midiout.send_message(button_deck_1_note_on)
input('Press Enter to start configuring button "' + button_name + '"-deck-1 NOTE OFF.\nPLEASE SETUP MIXXX LEARNING PROCESS')
midi_handler.midiout.send_message(button_deck_1_note_off)

input('Press Enter to start configuring button "' + button_name + '"-deck-2 NOTE ON.\nPLEASE SETUP MIXXX LEARNING PROCESS')
midi_handler.midiout.send_message(button_deck_2_note_on)
input('Press Enter to start configuring button "' + button_name + '"-deck-1 NOTE OFF.\nPLEASE SETUP MIXXX LEARNING PROCESS')
midi_handler.midiout.send_message(button_deck_2_note_off)
