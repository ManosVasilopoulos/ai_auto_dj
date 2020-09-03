from time import sleep
from numpy import ndarray as npndarray


class Pressings:

    def __init__(self, library_handler, decks, state):
        self.library_handler = library_handler
        self.decks = decks
        self.state = state

    # Buttons
    def scroll_up(self, times: int, see_scrolling=False):
        for i in range(times):
            self.library_handler.move_up()
            if see_scrolling:
                sleep(0.5)

    def scroll_down(self, times: int):
        for i in range(times):
            self.library_handler.move_down()
            sleep(0.2)

    def load_track(self, deck_number: int, track: npndarray):
        deck = self.decks[deck_number - 1]
        deck.load_track()
        self.state['side_' + str(deck_number)]['loaded_track'] = track
        sleep(0.2)

    def press_play(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.play_pause()
        sleep(0.2)

    def press_cue(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.cue()
        sleep(0.2)

    def press_sync(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.sync()
        sleep(0.2)

    def press_beat_sync(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.beat_sync()
        sleep(0.2)

    def reset_bpm(self, deck_number):
        deck = self.decks[deck_number - 1]
        deck.reset_bpm()
        sleep(0.2)

    def press_go_to_cue_and_play(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        deck.go_to_cue_and_play()
        sleep(0.2)
