import rtmidi

# CONFIGURE BUTTONS ONLY

midiin = rtmidi.MidiIn()
in_ports = midiin.get_ports()
midiout = rtmidi.MidiOut()
out_ports = midiout.get_ports()

outidx = 1

print(out_ports, outidx)
if outidx:
    midiout.open_port(outidx)
else:
    raise Exception('NO Output-PORTS FOUND')


msg = [0xB6, 64, 63]
print(msg)
input('Press Enter to send a rotary Message: ')
midiout.send_message(msg)

input('Final Enter')

del midiin
del midiout


