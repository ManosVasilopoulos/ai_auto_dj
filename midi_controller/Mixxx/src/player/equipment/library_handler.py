from midi_controller.Mixxx.src.player.midi.mappings import library_buttons
import rtmidi


class LibraryHandler:

    def __init__(self, midiout: rtmidi.MidiOut):
        self.midiout = midiout

    def __press_button(self, button_name: str):
        button_name_note_on = library_buttons[button_name]['master']['note_on']
        button_name_note_off = library_buttons[button_name]['master']['note_off']
        self.midiout.send_message(button_name_note_on)
        self.midiout.send_message(button_name_note_off)

    def move_down(self):
        self.__press_button('move_down')

    def move_up(self):
        self.__press_button('move_up')

    def move_focus(self):
        self.__press_button('move_focus')

    def move_focus_right_pane(self):
        self.__press_button('move_focus_right_pane')

    def move_focus_left_pane(self):
        self.__press_button('move_focus_left_pane')

    def sort_playlist_by_bpm(self):
        # Mixxx doesn't sort via MIDI, only but clicking
        pass

