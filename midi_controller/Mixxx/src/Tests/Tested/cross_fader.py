import time
from midi_out_port import get_midi_port

master_crossfader = [0xB0, 1, 63]

midiout, port_name = get_midi_port()

time.sleep(3)
print('Preparing master fader...')
for i in range(63, 128):
    print(i)
    master_crossfader = [0xB0, 1, i]
    midiout.send_message(master_crossfader)
    time.sleep(0.01)
print('Center --> Left...')
for i in range(127, -1, -1):
    print(i)
    master_crossfader = [0xB0, 1, i]
    midiout.send_message(master_crossfader)
    time.sleep(0.01)
print('Left --> Right...')

for i in range(0, 65):
    print(i)
    master_crossfader = [0xB0, 1, i]
    midiout.send_message(master_crossfader)
    time.sleep(0.01)
print('Right --> Center...')

midiout.close_port()