from poi_detector.src.models.locator_v2.model import Locator2
from .data_handler import Locator2DataHandler
from os import listdir as os_listdir
from os.path import join as os_path_join
from .predictions_processor import PredictionsProcessor
from pandas import DataFrame
from csv import QUOTE_NONNUMERIC

batch_size = 1
time_size = 1000
freq_size = 256
transform_type = 'melspectrogram'
window_size = 100


class PlaylistLocator2Predictor:

    def __init__(self, architecture_id, playlist_dir: str):
        self.playlist_dir = playlist_dir
        self.data_dir = os_path_join(playlist_dir, 'transforms', 'locator_v2_melspectrogram')

        self.locator = Locator2(architecture_id, batch_size, time_size, freq_size, transform_type, window_size)
        self.locator.load_trained_model()
        self.locator.cnn_model.summary()

        self.data_handler = Locator2DataHandler(self.playlist_dir, self.data_dir, time_size, freq_size, window_size,
                                                transform_type)
        self.pred_processor = PredictionsProcessor()

    def predict_4_poi_locations(self):
        playlist_transforms = os_listdir(self.data_dir)
        sections = {'id': [], 'Song': [], 'POIS': []}

        for i, song_transform_name in enumerate(playlist_transforms):
            print('------------------------------------------------------------------')
            print('Predictions of:', song_transform_name)

            x = self.data_handler.read_input(song_transform_name, 0, time_size)

            predictions = self.locator.predict(x)[0]

            cue = self.pred_processor.find_cue_peak(predictions) * window_size / 1000
            print('Cue point found:', cue)

            peaks = self.pred_processor.find_peaks(predictions)
            poi = self.__indexes_to_seconds(peaks)
            print('Peaks found:', poi)

            song_name = self.data_handler.extract_song_name(song_transform_name)
            sections['id'].append(i)
            sections['Song'].append(song_name)
            sections['POIS'].append(poi)
        return sections

    def save_playlist_predictions(self, playlist_sections: dict):
        df = DataFrame(playlist_sections)
        df.Song = df.Song.astype(str)
        df.POIS = df.POIS.astype(str)

        locator_v2_csv_file_path = os_path_join(self.playlist_dir, 'pois_locator_v2.csv')
        df.to_csv(locator_v2_csv_file_path, index=False, quotechar='"', quoting=QUOTE_NONNUMERIC)

        return locator_v2_csv_file_path

    def __indexes_to_seconds(self, poi_list: list):
        return [x * window_size / 1000 for x in poi_list]


if __name__ == '__main__':
    playlist_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\Mixxx\\5\\'
    playlist_locator = PlaylistLocator2Predictor(6, playlist_dir)
    playlist_sects = playlist_locator.predict_4_poi_locations()
    playlist_locator.save_playlist_predictions(playlist_sects)
