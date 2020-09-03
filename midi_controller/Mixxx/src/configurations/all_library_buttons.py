from midi_controller.Mixxx.src.player.midi.midi_handler import MidiHandler
from midi_controller.Mixxx.src.player.midi.mappings import library_buttons

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

for button_name in library_buttons:
    button_note_on = library_buttons[button_name]['master']['note_on']
    button_note_off = library_buttons[button_name]['master']['note_off']

    input('Press Enter to start configuring button "' + button_name + '" of Library NOTE ON.\nPLEASE SETUP MIXXX LEARNING PROCESS')
    midi_handler.midiout.send_message(button_note_on)
    input('Press Enter to start configuring button "' + button_name + '" of Library  NOTE OFF.\nPLEASE SETUP MIXXX LEARNING PROCESS')
    midi_handler.midiout.send_message(button_note_off)
