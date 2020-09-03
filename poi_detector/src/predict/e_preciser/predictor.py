from poi_detector.src.models.preciser_v1.model import Preciser
from .data_handler import PreciserDataHandler
from os.path import join as os_path_join
from pandas import DataFrame
from csv import QUOTE_NONNUMERIC


class PreciserPredictor:
    batch_size = 1
    time_size = 500
    freq_size = 256
    window_size = 10

    def __init__(self, architecture_id: int, playlist_dir: str, transform_type: str):

        self.playlist_dir = playlist_dir

        self.transform_type = transform_type

        self.__configure_transform_dims(transform_type)

        self.data_dir = os_path_join(playlist_dir, 'transforms', 'preciser_' + transform_type)

        self.preciser = Preciser(architecture_id,
                                 self.batch_size,
                                 self.time_size,
                                 self.freq_size,
                                 self.transform_type,
                                 self.window_size)

        self.preciser.load_trained_model()
        self.preciser.cnn_model.summary()
        self.data_handler = PreciserDataHandler(self.data_dir,
                                                self.time_size,
                                                self.freq_size,
                                                self.window_size,
                                                self.transform_type)

    # sections = {'id': [], 'Song': [], 'POIS': []}
    def predict_playlist_precise_poi(self, sections: dict):
        playlist_songs = sections['Song']
        df = DataFrame(sections)
        print('Sections Before:\n', df)

        new_sections = {'id': sections['id'],
                        'Song': sections['Song'],
                        'POIS': []}
        for i, song in enumerate(playlist_songs):
            precise_pois = []
            for poi in sections['POIS'][i]:
                precise_pois.append(self.predict_frame_offset(song, poi))
            new_sections['POIS'].append(precise_pois)

        df = DataFrame(new_sections)
        print('Sections After:\n', df)
        return new_sections

    def predict_frame_offset(self, song_name: str, poi_relative_location: float, return_offset=False):
        start_index, poi_relative_location = self.__get_start_index_and_fix_relative_poi(poi_relative_location)

        sub_transform = self.__get_input(song_name, start_index)

        prediction = self.preciser.predict(sub_transform)[0]
        offset = int(prediction * self.window_size * self.time_size) / 1000
        precise_poi = self.__calculate_precise_poi(poi_relative_location, offset)

        if return_offset:
            return offset, precise_poi
        else:
            return precise_poi

    def save_playlist_predictions(self, playlist_sections: dict):
        df = DataFrame(playlist_sections)
        df.Song = df.Song.astype(str)
        df.POIS = df.POIS.astype(str)

        preciser_csv_file_path = os_path_join(self.playlist_dir, 'pois_preciser.csv')
        df.to_csv(preciser_csv_file_path, index=False, quotechar='"', quoting=QUOTE_NONNUMERIC)

        return preciser_csv_file_path

    def __calculate_precise_poi(self, poi_relative_location: float, offset: float):
        if poi_relative_location == .0:
            return poi_relative_location + offset
        else:
            return poi_relative_location + offset - self.__index_to_seconds(self.time_size // 2)

    def __get_input(self, song_name: str, start_index: int):
        if '.jpg' not in song_name:
            song_name += '.jpg'
        return self.data_handler.read_input(song_name, start_index, start_index + self.time_size)

    def __get_start_index_and_fix_relative_poi(self, poi_relative_location):
        start_index = self.__seconds_to_index(poi_relative_location) - self.time_size // 2
        if start_index < 0:
            start_index = 0
            poi_relative_location = .0
        return start_index, poi_relative_location

    def __seconds_to_index(self, poi):
        return int(poi * 1000 / self.window_size)

    def __index_to_seconds(self, index):
        return index / (1000 / self.window_size)

    def __configure_params(self, time_size, freq_size, window_size):
        self.time_size = time_size
        self.freq_size = freq_size
        self.window_size = window_size

    def __configure_transform_dims(self, transform_type: str):
        if transform_type == 'spectrogram':
            self.__configure_params(500, 512, 10)
        elif transform_type == 'melspectrogram':
            self.__configure_params(500, 256, 10)
        elif transform_type == 'cqt':
            self.__configure_params(100, 108, 11.61)
        else:
            raise Exception(
                'PreciserPredictorError: there are no models trained with the transform "' + transform_type +
                '. Check for spelling errors!"')


if __name__ == '__main__':
    playlist_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\Mixxx\\3\\'
    predictor = PreciserPredictor(8, playlist_dir, 'cqt')
    track = '6ix9ine, Nicki Minaj - TROLLZ (with Nicki Minaj).wavpreciser_cqt.jpg'
    start_indexes = [0.5, 14.5, 20.7, 31.3, 44.9, 50.1, 69.0, 88.4]
    print('Predictions of', track)
    for start_index in start_indexes:
        predicted_offset = predictor.predict_frame_offset(track, start_index)
        print('Start Index:', start_index, 'Offset:', predicted_offset)
