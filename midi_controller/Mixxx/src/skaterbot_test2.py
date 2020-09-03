from player.metadata.metadata_handler import MetaDataHandler
import sys

playlist_name = sys.argv[1]

metadata_handler = MetaDataHandler(playlist_name)

print(metadata_handler.csv_handler.df)
