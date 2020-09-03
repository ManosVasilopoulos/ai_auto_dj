from os import listdir as oslistdir
from os.path import join as ospathjoin
from .csv_handler import CSVHandler
from .sql_handler import SQLHandler
from numpy import array as nparray
from numpy import argsort as npargsort


class MetaDataHandler:
    playlists_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\\Mixxx'

    def __init__(self, playlist_name: str, poi_csv_file: str):

        self.playlist_name = playlist_name
        self.playlist_path = ospathjoin(self.playlists_dir, str(playlist_name))
        self.csv_handler = CSVHandler(ospathjoin(self.playlist_path, poi_csv_file))
        self.sql_handler = SQLHandler()

    # Tested - OK
    def list_playlist_songs(self):
        files = oslistdir(self.playlist_path)
        song_files = []
        for file in files:
            file_is_song_type = ('.mp3' in file or '.MP3' in file) or ('.wav' in file or '.WAV' in file)
            if file_is_song_type:
                song_files.append(file)
        return song_files

    # Tested - OK
    def list_playlist_songs2(self):
        files = oslistdir(self.playlist_path)
        song_files = filter(lambda x: ('.mp3' in x or '.MP3' in x) or ('.wav' in x or '.WAV' in x), files)
        return [x for x in song_files]

    # Tested - OK
    def get_tracks_full_metadata(self):
        tracks_metadata = self.sql_handler.get_playlist_tracks_metadata(self.playlist_name)
        print(tracks_metadata)
        tracks_pois = self.csv_handler.get_dataframe_numpy()
        playlist_full_db = []
        for i, record in enumerate(tracks_pois):
            track_name = record[1]
            track_pois = record[2]
            track_bpm = tracks_metadata[track_name]['bpm']
            track_key = tracks_metadata[track_name]['key']
            track_duration = tracks_metadata[track_name]['duration']
            track_full_data = nparray([track_name, track_pois, track_bpm, track_key, track_duration])
            playlist_full_db.append(track_full_data)
        return nparray(playlist_full_db)

    # Tested - OK
    def sort_metadata_by_bpm(self, metadata):
        return metadata[npargsort(metadata[:, 2])]

    # Tested - OK
    def sort_metadata_by_filename(self, metadata):
        print(npargsort(metadata[:, 0]))
        return metadata[npargsort(metadata[:, 0])]
