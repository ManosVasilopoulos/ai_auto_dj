from midi_controller.Mixxx.src.player.midi.midi_handler import MidiHandler
from midi_controller.Mixxx.src.player.equipment.library_handler import LibraryHandler
from midi_controller.Mixxx.src.player.equipment.deck_handler import DeckHandler
from midi_controller.Mixxx.src.player.equipment.mixer_handler import MixerHandler
from .actions.movements import Movements
from .actions.setups import Setups
from .actions.pressings import Pressings

from numpy import ndarray as npndarray
from numpy import array as nparray
import rtmidi
from time import sleep
from time import time


class Mixx_DJ:
    midiout: rtmidi.MidiOut
    port_name: str

    # field "loaded_track"--> np.array(['track_name', pois, bpm, key])
    state = {
        'side_1': {
            'loaded_track': nparray([]),
            'fader_val': 127,
            'eq_hi_val': 64,
            'eq_mid_val': 64,
            'eq_low_val': 64,
            'filter': 64,
            'gain': 64
        },
        'side_2': {
            'deck_loaded': nparray([]),
            'fader_val': 127,
            'eq_hi_val': 64,
            'eq_mid_val': 64,
            'eq_low_val': 64,
            'filter': 64,
            'gain': 64
        },
        'master': {
            'crossfader_val': 64
        }
    }

    def __init__(self):

        self.midi_handler = MidiHandler()
        self.midi_handler.setup_midi_in_port('CHANGETHIS')
        self.midi_handler.setup_midi_out_port('LoopBe')

        self.deck1 = DeckHandler(self.midi_handler.midiout, 1)
        self.mixer = MixerHandler(self.midi_handler.midiout, 2)
        self.deck2 = DeckHandler(self.midi_handler.midiout, 2)

        self.ch_1 = self.mixer.channels[0]
        self.ch_2 = self.mixer.channels[1]
        self.channels = [self.ch_1, self.ch_2]

        self.decks = [self.deck1, self.deck2]

        print('Mixxx-DJ is using in-Port:', self.midi_handler.in_port_name)
        print('Mixxx-DJ is using out-Port:', self.midi_handler.out_port_name)
        self.library_handler = LibraryHandler(self.midi_handler.midiout)

        self.moves = Movements(self.mixer, self.channels, self.state)
        self.pressings = Pressings(self.library_handler, self.decks, self.state)
        self.setups = Setups(self.moves, self.pressings, self.decks)

    def swap_sides(self, current: int):
        if current == 1:
            return 2, 1
        elif current == 2:
            return 1, 2
        else:
            raise Exception('MixxxDJError: deck-number cannot be ' + str(current) + '. Only "1" or "2".')

    # Not Implemented - DO NOT USE
    def eject_current_track(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.eject_track()
        self.state['side_' + str(deck_number)]['loaded_track'] = nparray([])
        sleep(0.01)
        return 0.01

    # ACTIONS
    def move_to_start(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.jump_to_start()
        sleep(0.01)
        return 0.01

    def move_to_cue_point(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        pois = self.state['side_' + str(deck_number)]['loaded_track'][1]
        cue_point = pois[0]

        self.move_to_start(deck_number)
        print('Setting cue of deck-' + str(deck_number), 'at:', cue_point)
        deck.fast_forward(cue_point)
        sleep(0.01)
        return 0.02

    def get_tomix_time(self, side: int):
        pois = self.state['side_' + str(side)]['loaded_track'][1]
        return pois[2] - pois[0]

    """ NEED IMPLEMENTATION OF FOCUS ON RIGHT PANEL --> PRESSINGS """

    def focus_on_library(self):
        self.library_handler.move_focus()
        sleep(0.01)
        return 0.01

    # WRONG EQUATION CALCULATED - CALCULATES THE CORRECT AMOUNT OF TIME OF INTRO
    def get_tomix_time_modified(self, current_side: int, previous_mix_duration: float,
                                previous_pitch_perc: float):
        if self.state['side_' + str(current_side)]['loaded_track'].size == 0:
            pois_current = nparray([0, 0, 0, 0])
            previous_pitch_perc = 0
        else:
            pois_current = self.state['side_' + str(current_side)]['loaded_track'][1]

        current_tomix_duration = pois_current[2] - pois_current[0]
        calculated_to_mix_duration = (current_tomix_duration) - (previous_mix_duration) * (1 + previous_pitch_perc)
        print('Current song\'s mix duration:', current_tomix_duration)
        print('To-mix time calculated:', calculated_to_mix_duration)
        return calculated_to_mix_duration

    def get_end_of_mix_time(self, side: int):
        if self.state['side_' + str(side)]['loaded_track'].size == 0:
            pois_current = nparray([0, 0, 0, 0])
        else:
            pois_current = self.state['side_' + str(side)]['loaded_track'][1]
        return pois_current[3] - pois_current[2]

    def __get_pitch_perc(self, current_deck_number: int, next_deck_number: int):
        bpm_current = self.state['side_' + str(current_deck_number)]['loaded_track'][2]
        bpm_next = self.state['side_' + str(next_deck_number)]['loaded_track'][2]
        print('Pitch Moved by', bpm_current / bpm_next - 1, '%.')
        return bpm_current / bpm_next - 1

    def get_next_song_ready(self, deck_number: int, track: npndarray):
        self.pressings.load_track(deck_number, track)
        print('Loaded track on deck-' + str(deck_number))

        self.move_to_start(deck_number)
        print('Jumped to start (deck-' + str(deck_number) + ')')
        self.move_to_cue_point(deck_number)
        print('Move to cue point (deck-' + str(deck_number) + ')')
        self.pressings.press_cue(deck_number)
        print('Pressed cue (deck-' + str(deck_number) + ')')

        self.pressings.press_sync(deck_number)
        print('Pressed sync (deck-' + str(deck_number) + ')')

    def mix_two_songs(self, current_side: int, next_side: int, latency: float):
        start_time = time()
        pois_current = self.state['side_' + str(current_side)]['loaded_track'][1]
        pois_next = self.state['side_' + str(next_side)]['loaded_track'][1]

        pitch_perc = self.__get_pitch_perc(current_side, next_side)

        intro_next = pois_next[1] - pois_next[0]
        mix_current = pois_current[3] - pois_current[2]

        elapsed_time = time() - start_time

        if mix_current < intro_next * pitch_perc:
            sleep(mix_current)
            return mix_current, pitch_perc
        else:
            sleep(mix_current / 2 - elapsed_time - latency)
            start_time = time()
            self.pressings.press_go_to_cue_and_play(next_side)
            elapsed_time = time() - start_time
            sleep(mix_current / 2 - elapsed_time)

            waiting_time = mix_current / 2 - elapsed_time
            return waiting_time, pitch_perc
