from player.midi.midi_handler import MidiHandler
from player.midi.mappings import library_buttons
import sys

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

button_name = sys.argv[1]

button_note_on = library_buttons[button_name]['master']['note_on']
button_note_off = library_buttons[button_name]['master']['note_off']

input('Press Enter to start configuring button "' + button_name + '" of Library.\nPLEASE SETUP MIXXX LEARNING PROCESS')
midi_handler.midiout.send_message(button_note_on)
midi_handler.midiout.send_message(button_note_off)
