from midi_controller.Mixxx.src.player.midi.mappings import dj_buttons
import rtmidi
from numpy import ndarray as npndarray
from time import time
from time import sleep

class DeckHandler:
    midiout: rtmidi.MidiOut
    deck: int
    loaded_track: npndarray  # nparray([track_name, track_pois, track_bpm, track_key, track_duration])

    def set_loaded_track(self, loaded_track: npndarray):
        self.loaded_track = loaded_track

    def __init__(self, midiout: rtmidi.MidiOut, deck: int):
        self.midiout = midiout
        self.deck = deck

    def __press_button(self, button_name: str, value=127):
        button_name_note_on = dj_buttons[button_name]['deck_' + str(self.deck)]['note_on']
        button_name_note_on[2] = value
        button_name_note_off = dj_buttons[button_name]['deck_' + str(self.deck)]['note_off']
        button_name_note_off[2] = value
        self.midiout.send_message(button_name_note_on)
        self.midiout.send_message(button_name_note_off)

    def fast_forward(self, time_interval: float):
        fast_forward_note_on = dj_buttons['fast_forward']['deck_' + str(self.deck)]['note_on']
        fast_forward_note_off = dj_buttons['fast_forward']['deck_' + str(self.deck)]['note_off']
        start_time = time()
        self.midiout.send_message(fast_forward_note_on)
        elapsed_time = time() - start_time
        sleep((time_interval - elapsed_time) / 4)       # we divide by 4 because it ffs times-4
        self.midiout.send_message(fast_forward_note_off)

    def fast_rewind(self, time_interval: float):
        fast_rewind_note_on = dj_buttons['fast_rewind']['deck_' + str(self.deck)]['note_on']
        fast_rewind_note_off = dj_buttons['fast_rewind']['deck_' + str(self.deck)]['note_off']
        start_time = time()
        self.midiout.send_message(fast_rewind_note_on)
        elapsed_time = time() - start_time
        sleep((time_interval - elapsed_time) / 4)
        self.midiout.send_message(fast_rewind_note_off)

    def play_pause(self):
        self.__press_button('play_pause')

    # Tested - OK
    def cue(self):
        self.__press_button('cue')

    # Tested - OK
    def jump_to_start(self):
        self.__press_button('jump_to_start')

    def flanger(self):
        self.__press_button('flanger')

    # Tested - OK
    def adjust_speed_slower(self):
        self.__press_button('adjust_speed_slower')

    # Tested - OK
    def adjust_speed_faster(self):
        self.__press_button('adjust_speed_faster')

    def temp_decrease_speed(self):
        self.__press_button('temp_decrease_speed')

    def temp_increase_speed(self):
        self.__press_button('temp_increase_speed')

    # Tested - NOT OK
    def play_reverse(self):
        self.__press_button('play_reverse')

    # Tested - OK
    def stop_and_jump_to_start(self):
        self.__press_button('stop_and_jump_to_start')

    def strip_search(self, seconds):
        # This process moves the current track-position at the end (maybe cause it's configured as button)
        duration = self.loaded_track[4]
        step = duration / 127
        value = int(seconds // step)
        self.__press_button('strip_search')

    def bpm_plus_01(self):
        self.__press_button('bpm_plus_0.1')

    def bpm_minus_01(self):
        self.__press_button('bpm_minus_0.1')

    # Tested - OK
    def sync(self):
        self.__press_button('sync')

    def key_lock(self):
        self.__press_button('key_lock')

    def match_key(self):
        self.__press_button('match_key')

    def reset_key(self):
        self.__press_button('reset_key')

    # Tested - OK
    def beat_sync(self):
        self.__press_button('beat_sync')

    # Tested - OK
    def beat_loop_16(self):
        self.__press_button('beat_loop_16')

    # Tested - OK
    def quantize(self):
        self.__press_button('quantize')

    # Tested - OK
    def load_track(self):
        self.__press_button('load_track')

    # Tested - OK
    def reset_bpm(self):
        self.__press_button('reset_speed')

    def go_to_cue_and_play(self):
        self.__press_button('go_to_cue_and_play')
