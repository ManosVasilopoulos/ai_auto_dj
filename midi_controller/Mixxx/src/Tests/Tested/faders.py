import time
from midi_out_port import get_midi_port

left_fader = [0xB0, 2, 63]
right_fader = [0xB0, 3, 63]

midiout, port_name = get_midi_port()

time.sleep(3)
print('Preparing to start Testing LEFT FADER...')
for i in range(127, -1, -1):
    print(i)
    left_fader[2] = i
    midiout.send_message(left_fader)
    time.sleep(0.005)
print('Up --> Down...DONE')

for i in range(0, 128):
    print(i)
    left_fader[2] = i
    midiout.send_message(left_fader)
    time.sleep(0.005)
print('Down --> Up...DONE')

time.sleep(3)
print('Preparing to start Testing RIGHT FADER...')
for i in range(127, -1, -1):
    print(i)
    right_fader[2] = i
    midiout.send_message(right_fader)
    time.sleep(0.005)
print('Up --> Down...DONE')

for i in range(0, 128):
    print(i)
    right_fader[2] = i
    midiout.send_message(right_fader)
    time.sleep(0.005)
print('Down --> Up...DONE')

midiout.close_port()
