from player.equipment.library_handler import LibraryHandler
from player.midi.midi_handler import MidiHandler
from time import sleep

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

library_handler = LibraryHandler(midi_handler.midiout)
input('Wait for button setup...Press Enter when ready...')
sleep(3)
for i in range(5):
    library_handler.move_focus()
    sleep(1)
    library_handler.move_focus_right_pane()
    sleep(1)
    library_handler.move_focus_left_pane()
    sleep(1)

midi_handler.close_all_ports()