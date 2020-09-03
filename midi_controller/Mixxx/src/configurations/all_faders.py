from midi_controller.Mixxx.src.player.midi.midi_handler import MidiHandler
from midi_controller.Mixxx.src.player.midi.mappings import faders
from .helper import move_fader

midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

crossfader = faders['crossfader']['master']['control_change']
input('Press Enter to start configuring fader "crossfader".')
move_fader(midi_handler.midiout, crossfader)

fader_ch_1 = faders['fader']['channel_1']['control_change']
fader_ch_2 = faders['fader']['channel_2']['control_change']

input('Press Enter to start configuring fader "fader"-channel-1')
move_fader(midi_handler.midiout, fader_ch_1)

input('Press Enter to start configuring fader "fader"-channel-2')
move_fader(midi_handler.midiout, fader_ch_2)
