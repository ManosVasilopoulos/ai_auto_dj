import rtmidi

def get_midi_port():
    midiin = rtmidi.MidiIn()
    available_ports = midiin.get_ports()

    port_name = None
    for i, port in enumerate(available_ports):
        if 'LPD8' in port:
            port_name = port
            midiin.open_port(i)
    if not port_name:
        raise Exception('Main port not found. Exiting...')
    return midiin, port_name