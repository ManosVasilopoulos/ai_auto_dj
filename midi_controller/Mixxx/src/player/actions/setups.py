from time import sleep

class Setups:

    def __init__(self, movements, pressings, decks):
        self.movements = movements
        self.pressings = pressings
        self.decks = decks

    # SETUPS
    def setup_mixer(self):
        print('Getting ready to setup mixer.')
        sleep(2)

        self.setup_channel(1)
        self.setup_channel(2)

        self.movements.move_crossfader(64)

    def setup_channel(self, channel: int):
        self.movements.move_fader_up(channel)
        print('Moved Fader-' + str(channel), 'up.')
        sleep(0.2)

        self.movements.move_eq_hi(channel, 64)
        print('Moved EQ-Hi-' + str(channel), 'to middle position.')
        sleep(0.2)
        self.movements.move_eq_mid(channel, 64)
        print('Moved EQ-Mid-' + str(channel), 'to middle position.')
        sleep(0.2)
        self.movements.move_eq_low(channel, 64)
        print('Moved EQ-Low-' + str(channel), 'to middle position.')
        sleep(0.2)
        self.movements.move_filter(channel, 64)
        print('Moved Filter-' + str(channel), 'to middle position.')
        sleep(0.2)

    def setup_deck(self, deck_number: int):
        deck = self.decks[deck_number - 1]
        print('Getting ready to setup deck-' + str(deck_number))
        sleep(0.5)

        deck.key_lock()
        sleep(0.1)
        print('Activated "key_lock".')
        deck.reset_bpm()
        sleep(0.1)
        print('Reset "bpm".')
        deck.quantize()
        sleep(0.1)
        print('Activated "quantize".')

