import rtmidi
import mido
import time

# TEST CONFIGURED BUTTONS ONLY

################################################
# Open In and Out Ports
midiout = rtmidi.MidiOut()
out_ports = midiout.get_ports()

print(out_ports)
outidx = 1

for i, port in enumerate(out_ports):
    if 'Configuration' in port:
        outport_name = port
        outidx = i

if outidx:
    midiout.open_port(outidx)
else:
    raise Exception('NO Output-PORTS FOUND')

time.sleep(3)
##################################################
# Browse Forward
for i in range(2):
    msg = [0xB0, 1, 65]
    print(msg)
    midiout.send_message(msg)
    time.sleep(0.1)

####################################################
# Load deck 1
msg = [0x90, 88, 112]
print('Sending message: ' + str(msg))
midiout.send_message(msg)
time.sleep(0.01)
msg = [0x80, 88, 0]
midiout.send_message(msg)
time.sleep(1)
print('Pressed Load on Deck 1')

####################################################
# Press Master Tempo
msg = [0x90, 70, 112]
print('Sending message: ' + str(msg))
midiout.send_message(msg)
time.sleep(0.01)
msg = [0x80, 70, 0]
midiout.send_message(msg)
time.sleep(1)
print('Pressed Load on Deck 1')

####################################################
# JumpToTrackStart
msg = [0x90, 64, 112]
print('Sending message: ' + str(msg))
midiout.send_message(msg)
time.sleep(0.01)
msg = [0x80, 64, 0]
midiout.send_message(msg)
print('Pressed Cue')
time.sleep(1)

####################################################
# Press Cue
msg = [0x90, 62, 112]
print('Sending message: ' + str(msg))
midiout.send_message(msg)
time.sleep(0.01)
msg = [0x80, 62, 0]
midiout.send_message(msg)
print('Pressed Cue')
time.sleep(1)

####################################################
# SearchFwd on Track
for i in range(150):
    msg = [0x90, 78, 112]
    print('Sending message: ' + str(msg))
    midiout.send_message(msg)
    time.sleep(0.005)
    msg = [0x80, 78, 0]
    midiout.send_message(msg)
    print('Pressed SearchFwd')
    time.sleep(0.005)

####################################################
# Press Cue
msg = [0x90, 62, 112]
print('Sending message: ' + str(msg))
midiout.send_message(msg)
time.sleep(0.01)
msg = [0x80, 62, 0]
midiout.send_message(msg)
print('Pressed Cue')
time.sleep(1)

####################################################
# Press Play
msg = [0x90, 58, 112]
print('Sending message: ' + str(msg))
midiout.send_message(msg)
time.sleep(0.01)
msg = [0x80, 58, 0]
midiout.send_message(msg)
print('Pressed Play')
time.sleep(1)

del midiout
print('Closed Port.')
