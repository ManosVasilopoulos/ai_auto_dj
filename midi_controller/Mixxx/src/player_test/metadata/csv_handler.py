from player.metadata.csv_handler import CSVHandler

playlist_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Playlists\\Mixxx\\1'

csv_handler = CSVHandler(playlist_dir)

dict_csv = csv_handler.get_dataframe_dictionary()
numpy_csv = csv_handler.get_dataframe_numpy()

print('DATAFRAME:')
print(csv_handler.df)
print('\nDictionary:')
print(dict_csv)
print('\nNumpy Array:')
print(numpy_csv)
