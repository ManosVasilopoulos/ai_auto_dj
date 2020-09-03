import mido
import rtmidi
import time
from rtmidi.midiutil import open_midiinput

midiin = rtmidi.MidiIn()
in_ports = midiin.get_ports()
midiout = rtmidi.MidiOut()
out_ports = midiout.get_ports()

print(in_ports, out_ports)

with mido.open_input(in_ports[0]) as inport:
    counter = 0
    for msg in inport:
        print(msg)
        counter += 1
        if counter >= 150:
            break

del midiin
del midiout
