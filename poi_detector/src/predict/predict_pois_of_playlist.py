from .a_decode_playlist.playlist_decoder import decode_playlist
from .b_transform_playlist.playlist_transformer import transform_playlist
from .d_locator_v2.predictor import PlaylistLocator2Predictor
from .e_preciser.predictor import PreciserPredictor
from os.path import join as os_path_join
from sys import argv as sys_argv
from pandas import DataFrame


def predict_poi_and_save_in_csv(playlist_name):
    base_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\\Mixxx\\'
    playlist_name = playlist_name
    playlist_path = os_path_join(base_dir, playlist_name)

    # Step 1
    print('----------------Decoding MP3 files to WAV----------------')
    playlist = decode_playlist(playlist_path)
    # Step 2
    if len(playlist) > 0:
        print('--------------Creating Transforms from WAVs--------------')
        transform_playlist(playlist_path)
    else:
        print('----------Skipped Creating Transforms from WAVs----------')

    # Step 3
    print('--------------Predicting Relative Locations--------------')
    playlist_locator = PlaylistLocator2Predictor(6, playlist_path)
    playlist_sections = playlist_locator.predict_4_poi_locations()
    df = DataFrame(playlist_sections)
    print('BEFORE ALL:\n', df)
    loc_csv_path = playlist_locator.save_playlist_predictions(playlist_sections)
    # Step 4
    print('----------Predicting Precise Points of Interest----------')
    song_preciser = PreciserPredictor(8, playlist_path, 'cqt')
    new_playlist_sections = song_preciser.predict_playlist_precise_poi(playlist_sections)
    prec_csv_path = song_preciser.save_playlist_predictions(new_playlist_sections)

    return (loc_csv_path, playlist_sections), (prec_csv_path, new_playlist_sections)


if __name__ == '__main__':
    playlist_name = sys_argv[1]
    predict_poi_and_save_in_csv(playlist_name)
