import mido
import rtmidi
import time

midiin = rtmidi.MidiIn()
in_ports = midiin.get_ports()
midiout = rtmidi.MidiOut()
out_ports = midiout.get_ports()

print(in_ports, out_ports)
print(mido.get_output_names())