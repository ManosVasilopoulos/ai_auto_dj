from playlist import Mixx_DJ
import time

dj = Mixx_DJ()

deck = 1

hold_duration = 0.5
for i in range(1):
    dj.step_forward(deck, hold_duration)
    time.sleep(1)
    print('New Step')
