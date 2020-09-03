from player.midi.midi_handler import MidiHandler
from player.midi.mappings import faders
import sys
from .helper import move_fader


midi_handler = MidiHandler()
midi_handler.setup_midi_out_port('LoopBe')

fader_name = sys.argv[1]

if fader_name == 'crossfader':
    crossfader = faders[fader_name]['master']['control_change']
    input('Press Enter to start configuring fader "' + fader_name + '".')
    move_fader(midi_handler.midiout, crossfader)
    pass
else:

    fader_ch_1 = faders[fader_name]['channel_1']['control_change']
    fader_ch_2 = faders[fader_name]['channel_2']['control_change']

    input('Press Enter to start configuring fader "' + fader_name + '"-channel-1')
    move_fader(midi_handler.midiout, fader_ch_1)

    input('Press Enter to start configuring fader "' + fader_name + '"-channel-2')
    move_fader(midi_handler.midiout, fader_ch_2)
