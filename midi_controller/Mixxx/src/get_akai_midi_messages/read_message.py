from .midi_in_port import get_midi_port

midiin, port_name = get_midi_port()
print(port_name)

while 1:
    try:
        message = midiin.get_message()
        if message:
            print(message)
    except KeyboardInterrupt:
        break

midiin.close_port()
