import time
import rtmidi


class RekordboxHandler():

    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.out_ports = self.midiout.get_ports()

    def sort_by_bpm(self):
        msg = [0x90, 90, 112]
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, 90, 112]
        self.midiout.send_message(msg)
        time.sleep(0.01)

        # sum of delay 0.02
        return 0.02

    def load_track_on_deck(self, deck_id):
        if deck_id == 1:
            ctrl = 88
        elif deck_id == 2:
            ctrl = 89
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, ctrl, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.1)
        msg = [0x80, ctrl, 0]
        self.midiout.send_message(msg)
        time.sleep(0.1)
        print('Pressed Load on Deck-' + str(deck_id))

        # sum of delay 0.02
        return 0.2

    def browse_to_next(self):
        # Browse Forward
        msg = [0xB6, 64, 65]
        print(msg)
        self.midiout.send_message(msg)
        time.sleep(0.01)

        # sum of delay 0.001
        return 0.01

    def browse_to_previous(self):
        # Browse Forward
        msg = [0xB6, 64, 63]
        print(msg)
        self.midiout.send_message(msg)
        time.sleep(0.01)

        # sum of delay 0.001
        return 0.01

    def master_tempo(self, deck_id):
        if deck_id == 1:
            mt = 70
        elif deck_id == 2:
            mt = 71
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, mt, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, 70, 0]
        self.midiout.send_message(msg)
        time.sleep(0.01)
        print('Pressed Master Tempo on Deck-' + str(deck_id))

        return 0.02

    def set_cue(self, deck_id, cue_point):
        timestep = 6.667
        time_moved = 0.0
        delay = 0.0
        if deck_id == 1:
            note_fwd = 78
        elif deck_id == 2:
            note_fwd = 79
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        # SearchFwd
        while time_moved < cue_point * 1000:
            msg = [0x90, note_fwd, 112]
            print('Sending message: ' + str(msg))
            self.midiout.send_message(msg)
            time.sleep(0.02)
            msg = [0x80, note_fwd, 0]
            self.midiout.send_message(msg)
            print('Pressed SearchFwd')
            time.sleep(0.02)
            time_moved += timestep

            delay += 0.04

        print('Actual Cue Point: ' + str(cue_point * 1000))
        print('Time Moved: ' + str(time_moved - timestep))
        print('Cue point MOD timestep: ' + str((cue_point*1000)%timestep))
        extra_delay = self.press_cue(deck_id)
        delay += extra_delay
        # sum of delay
        return delay

    def things_to_do(self, deck_id):
        if deck_id == 1:
            print('')
        elif deck_id == 2:
            print('')
        return 0

    def fader_up_and_sync(self, deck_id):
        if deck_id == 1:
            ctrl = 1
        elif deck_id == 2:
            ctrl = 2
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        for i in range(63):
            msg = [0xB1, ctrl, i]
            self.midiout.send_message(msg)
            time.sleep(0.01)

        extra_delay = self.press_sync(deck_id)
        for i in range(64, 128):
            msg = [0xB1, ctrl, i]
            self.midiout.send_message(msg)
            time.sleep(0.01)

        # sum of delay
        return 0.01*128 + extra_delay

    def fader_up(self, deck_id):
        if deck_id == 1:
            ctrl = 1
        elif deck_id == 2:
            ctrl = 2
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        for i in range(128):
            msg = [0xB1, ctrl, i]
            self.midiout.send_message(msg)
            time.sleep(0.01)

        # sum of delay
        return 0.01*128

    def fader_down(self, deck_id):
        if deck_id == 1:
            ctrl = 1
        elif deck_id == 2:
            ctrl = 2
        else:
            raise Exception('WRONG DECK-ID NUMBER.')
        # Fader Down
        for i in range(127, -1, -1):
            msg = [0xB1, ctrl, i]
            self.midiout.send_message(msg)
            time.sleep(0.01)

        return 0.01 * 128

    def press_play(self, deck_id):
        if deck_id == 1:
            note_play = 58
        elif deck_id == 2:
            note_play = 59
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, note_play, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, note_play, 0]
        self.midiout.send_message(msg)
        print('Pressed Play')
        time.sleep(0.01)

        # sum of delay
        return 0.02

    def press_sync(self, deck_id):
        if deck_id == 1:
            note_sync = 82
        elif deck_id == 2:
            note_sync = 83
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, note_sync, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, note_sync, 0]
        self.midiout.send_message(msg)
        print('Pressed Play')
        time.sleep(0.01)

        return 0.02

    def press_cue(self, deck_id):
        if deck_id == 1:
            note_cue = 62
        elif deck_id == 2:
            note_cue = 63
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, note_cue, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, note_cue, 0]
        self.midiout.send_message(msg)
        print('Pressed Cue')
        time.sleep(0.01)

        return 0.02

    def tempo_reset(self, deck_id):
        if deck_id == 1:
            note_reset = 84
        elif deck_id == 2:
            note_reset = 85
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, note_reset, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, note_reset, 0]
        self.midiout.send_message(msg)
        print('Pressed Cue')
        time.sleep(0.01)

        return 0.02

    def jump_to_track_start(self, deck_id):
        if deck_id == 1:
            note_jump_start = 64
        elif deck_id == 2:
            note_jump_start = 65
        else:
            raise Exception('WRONG DECK-ID NUMBER.')

        msg = [0x90, note_jump_start, 112]
        print('Sending message: ' + str(msg))
        self.midiout.send_message(msg)
        time.sleep(0.01)
        msg = [0x80, 64, 0]
        self.midiout.send_message(msg)
        print('Jumped To Start')
        time.sleep(0.01)

        return 0.02

    def open_port(self):
        self.midiout.open_port(1)

    def close_port(self):
        del self.midiout
