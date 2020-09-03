from player.metadata.sql_handler import SQLHandler
playlist_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\\Mixxx\\'

sql_handler = SQLHandler()

a = sql_handler.get_playlist_id('Test')

track_ids = sql_handler.get_playlist_tracks('Test')

full_meta = sql_handler.get_track_metadata(631)
print(full_meta)

