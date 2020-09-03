from  player.metadata.metadata_handler import MetaDataHandler

metadata_handler = MetaDataHandler('1')

filtered = metadata_handler.list_playlist_songs()
filtered2 = metadata_handler.list_playlist_songs2()

playlist_db = metadata_handler.get_tracks_full_metadata()
print(metadata_handler.sort_metadata_by_filename(playlist_db))
