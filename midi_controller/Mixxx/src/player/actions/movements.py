class Movements:

    def __init__(self, mixer, channels, state):
        self.mixer = mixer
        self.state = state
        self.channels = channels

    # FADERS AND KNOBS MOVEMENTS
    def move_crossfader(self, to_position=64, duration=0.5):
        current_position = self.state['master']['crossfader_val']
        self.mixer.move_crossfader(current_position, to_position, duration)
        return duration

    def move_eq_hi(self, channel: int, to_position=64, duration=0.5):
        ch = self.channels[channel - 1]
        current_position = self.state['side_' + str(channel)]['eq_hi_val']
        ch.move_eq_hi_knob(current_position, to_position, duration)
        self.state['side_' + str(channel)]['eq_hi_val'] = to_position
        return duration

    def move_eq_mid(self, channel: int, to_position=64, duration=0.5):
        ch = self.channels[channel - 1]
        current_position = self.state['side_' + str(channel)]['eq_mid_val']
        ch.move_eq_mid_knob(current_position, to_position, duration)
        self.state['side_' + str(channel)]['eq_mid_val'] = to_position
        return duration

    def move_eq_low(self, channel: int, to_position=64, duration=0.5):
        ch = self.channels[channel - 1]
        current_position = self.state['side_' + str(channel)]['eq_low_val']
        ch.move_eq_low_knob(current_position, to_position, duration)
        self.state['side_' + str(channel)]['eq_low_val'] = to_position
        return duration

    def move_filter(self, channel: int, to_position=64, duration=0.5):
        ch = self.channels[channel - 1]
        current_position = self.state['side_' + str(channel)]['filter']
        ch.move_filter_knob(current_position, to_position, duration)
        self.state['side_' + str(channel)]['eq_low_val'] = to_position
        return duration

    def move_gain(self, channel: int, to_position=64, duration=0.5):
        ch = self.channels[channel - 1]
        current_position = self.state['side_' + str(channel)]['gain']
        ch.move_filter_knob(current_position, to_position, duration)
        self.state['side_' + str(channel)]['eq_low_val'] = to_position
        return duration

    def move_fader_up(self, channel: int, to_position=128, duration=2):
        ch = self.channels[channel - 1]

        current_position = self.state['side_' + str(channel)]['fader_val']
        if current_position > to_position:
            current_position = to_position

        ch.move_fader(current_position, to_position, duration)

        self.state['side_' + str(channel)]['fader_val'] = to_position - 1
        return duration

    def move_fader_down(self, channel: int, to_position=-1, duration=2):
        ch = self.channels[channel - 1]

        current_position = self.state['side_' + str(channel)]['fader_val']
        if to_position > current_position:
            to_position = current_position
        ch.move_fader(current_position, to_position, duration)

        self.state['side_' + str(channel)]['fader_val'] = to_position + 1
        return duration
