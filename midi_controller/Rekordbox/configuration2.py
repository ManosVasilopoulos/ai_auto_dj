import rtmidi

# CONFIGURE BUTTONS ONLY

midiin = rtmidi.MidiIn()
in_ports = midiin.get_ports()
midiout = rtmidi.MidiOut()
out_ports = midiout.get_ports()

for i, port in enumerate(in_ports):
    if 'Configuration' in port:
        inport_name = port
        inidx = i
        print(port, i)

for i, port in enumerate(out_ports):
    if 'Configuration' in port:
        outport_name = port
        outidx = i

print(in_ports, inidx)
if inidx:
    midiin.open_port(inidx)
else:
    raise Exception('NO Output-PORTS FOUND')


print(out_ports, outidx)
if outidx:
    midiout.open_port(outidx)
else:
    raise Exception('NO Output-PORTS FOUND')

for i in range(35):
    note = i + 60
    print(note)
    msg = [0x90, note, 112]
    print(msg)
    input('Press Enter to send a note_on Message: ')
    midiout.send_message(msg)
    counter = 0
    while counter < 100:
        try:
            message, delta_time = midiin.get_message()
        except:
            print('Breaking')
            break
        print('Counter :' + str(counter))
        print('Input message: ' + str(message))
        counter += 1
    """
    input('Press Enter to send a note_off Message: ')
    msg = [0x80, note, 0]
    print(msg)
    midiout.send_message(msg)
    """

del midiout
del midiin