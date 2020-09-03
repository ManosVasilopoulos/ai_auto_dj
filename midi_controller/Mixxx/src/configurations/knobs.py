from midi_controller.Mixxx.src.player.midi.midi_handler import MidiHandler
from midi_controller.Mixxx.src.player.midi.mappings import knobs
import sys
from .helper import move_knob

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

knob_name = sys.argv[1]

knob_ch_1 = knobs[knob_name]['channel_1']['control_change']
knob_ch_2 = knobs[knob_name]['channel_2']['control_change']

input('Press Enter to start configuring knob "' + knob_name + '"-channel-1')
move_knob(midi_handler.midiout, knob_ch_1)

input('Press Enter to start configuring knob "' + knob_name + '"-channel-2')
move_knob(midi_handler.midiout, knob_ch_2)
