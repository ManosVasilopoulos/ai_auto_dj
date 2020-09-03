from rtmidi import MidiIn, MidiOut


class MidiHandler:
    midiin: MidiIn
    midiout: MidiOut
    in_port_name = ''
    out_port_name = ''

    def __init__(self):
        self.midiin = MidiIn()
        self.midiout = MidiOut()

    def setup_midi_in_port(self, port_name: str):
        available_ports = self.midiin.get_ports()

        found_port = False
        for i, port in enumerate(available_ports):
            if port_name in port:
                port_name = port
                self.midiin.open_port(i)
                found_port = True
        if not found_port:
            print('Main In-port not found. Exiting...')
            port_name = ''
        self.in_port_name = port_name

    def setup_midi_out_port(self, port_name: str):
        available_ports = self.midiout.get_ports()

        found_port = False
        for i, port in enumerate(available_ports):
            if port_name in port:
                port_name = port
                self.midiout.open_port(i)
                found_port = True
        if not found_port:
            print('Main out-Port not found. Exiting...')
            port_name = ''
        self.out_port_name = port_name

    def close_all_ports(self):
        self.midiin.close_port()
        self.midiout.close_port()
