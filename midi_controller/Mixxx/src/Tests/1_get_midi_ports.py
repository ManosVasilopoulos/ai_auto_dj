import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

main_out_port = None
for port in available_ports:
    if 'LoopBe' in port:
        main_out_port = port
if not main_out_port:
    raise Exception('Main port not found. Exiting...')
