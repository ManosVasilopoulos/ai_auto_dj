from rtmidi import MidiOut
import time


def move_knob(midi_out: MidiOut, knob_message: list):
    for i in range(knob_message[2], -1, -1):
        knob_message[2] = i
        midi_out.send_message(knob_message)
        time.sleep(0.01)
    print('Up --> Down...DONE')

    for i in range(0, 128):
        knob_message[2] = i
        midi_out.send_message(knob_message)
        time.sleep(0.01)
    print('Down --> Up...DONE')


def move_fader(midi_out: MidiOut, fader_message: list):
    for i in range(fader_message[2], -1, -1):
        fader_message[2] = i
        midi_out.send_message(fader_message)
        time.sleep(0.01)
    print('Up --> Down...DONE')

    for i in range(0, 128):
        fader_message[2] = i
        midi_out.send_message(fader_message)
        time.sleep(0.01)
    print('Down --> Up...DONE')
