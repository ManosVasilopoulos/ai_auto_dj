from poi_detector.src.models.locator_v1.model import Locator1
from .data_handler import Locator1DataHandler
from os import listdir as os_listdir
from numpy import sort as np_sort

_id = 4
batch_size = 1
time_size = 100
freq_size = 108
transform_type = 'cqt'
window_size = 11.61
data_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\Mixxx\\3\\transforms\\locator_v1_cqt\\'

locator = Locator1(_id, batch_size, time_size, freq_size, transform_type, window_size)
locator.load_trained_model()
locator.rnn.decoder.summary()

data_handler = Locator1DataHandler(data_dir, time_size, freq_size, window_size, transform_type)
playlist = os_listdir(data_dir)
for song_name in playlist:
    print('Predictions of:', song_name)
    x = data_handler.read_input(song_name, 0, data_handler.max_time_steps * time_size)
    print(x.shape)
    predictions = locator.predict(x)[0]
    print('Time step duration:', (time_size / 1000) * window_size, 'seconds.')
    print('Time steps:', predictions.size)
    print('Indexes:', predictions.argsort()[-8:][::-1])
    print('Start of Intervals:', np_sort(predictions.argsort()[-8:][::-1] * window_size * (time_size / 1000)))
    print('------------------------------------------------------------------')
