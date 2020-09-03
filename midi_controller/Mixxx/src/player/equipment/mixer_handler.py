from rtmidi import MidiOut
from midi_controller.Mixxx.src.player.midi.mappings import faders
from midi_controller.Mixxx.src.player.midi.mappings import knobs
from time import sleep as timesleep


class MixerHandler:
    midiout: MidiOut
    channels = []

    def __init__(self, midiout: MidiOut, n_channels: int):
        self.midiout = midiout
        for i in range(n_channels):
            self.channels.append(MixerChannelHandler(midiout, i + 1))

    # Linear Movement
    def __move_control(self, fader_message: list, from_val: int, to_val: int, duration=.0):
        interval = duration / 128
        for i in range(from_val, to_val):
            fader_message[2] = i
            self.midiout.send_message(fader_message)
            timesleep(interval)

    def move_crossfader(self, from_val: int, to_val: int, duration=.0):
        crossfader_message = faders['crossfader']['master']['control_change']
        self.__move_control(crossfader_message, from_val, to_val, duration)


class MixerChannelHandler:
    midiout: MidiOut
    channel: int

    def __init__(self, midiout: MidiOut, channel: int):
        if not 1 <= channel <= 4:
            raise Exception('MixerHandlerError: mixer\'s "channel" cannot be less than 1 or greater than 2.'
                            ' Given value: ' + str(channel))
        self.midiout = midiout
        self.channel = channel

    # Linear Movement
    def __move_control(self, fader_message: list, from_val: int, to_val: int, duration=.0):
        interval = duration / 128
        if from_val <= to_val:
            for i in range(from_val, to_val):
                fader_message[2] = i
                self.midiout.send_message(fader_message)
                timesleep(interval)
        else:
            for i in range(from_val, to_val, -1):
                fader_message[2] = i
                self.midiout.send_message(fader_message)
                timesleep(interval)

    def move_fader(self, from_val: int, to_val: int, duration=.0):
        fader_message = faders['fader']['channel_' + str(self.channel)]['control_change']
        self.__move_control(fader_message, from_val, to_val, duration)

    def move_eq_low_knob(self, from_val: int, to_val: int, duration=.0):
        knob_message = knobs['low_eq']['channel_' + str(self.channel)]['control_change']
        self.__move_control(knob_message, from_val, to_val, duration)

    def move_eq_mid_knob(self, from_val: int, to_val: int, duration=.0):
        knob_message = knobs['mid_eq']['channel_' + str(self.channel)]['control_change']
        self.__move_control(knob_message, from_val, to_val, duration)

    def move_eq_hi_knob(self, from_val: int, to_val: int, duration=.0):
        knob_message = knobs['hi_eq']['channel_' + str(self.channel)]['control_change']
        self.__move_control(knob_message, from_val, to_val, duration)

    def move_filter_knob(self, from_val: int, to_val: int, duration=.0):
        knob_message = knobs['filter']['channel_' + str(self.channel)]['control_change']
        self.__move_control(knob_message, from_val, to_val, duration)

    def move_gain_knob(self, from_val: int, to_val: int, duration=.0):
        knob_message = knobs['gain']['channel_' + str(self.channel)]['control_change']
        self.__move_control(knob_message, from_val, to_val, duration)
