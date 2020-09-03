import pandas as pd
from numpy import array as nparray

class CSVHandler:
    df: pd.DataFrame

    def __init__(self, poi_csv_path: str):
        self.df = self.read_csv_to_dataframe(poi_csv_path)

    # Tested - OK
    def __find_csv_file(self, files: list):
        for file in files:
            if '.csv' in file:
                return file
        raise Exception('CSVHandlerError: NO "csv" files found in this directory."')

    # Tested - OK
    def read_csv_to_dataframe(self, csv_playlist_path: str):
        df = pd.read_csv(csv_playlist_path)
        df['POIS'] = df['POIS'].apply(func=eval)
        df['POIS'] = df['POIS'].apply(func=nparray)
        return df

    def get_dataframe_dictionary(self):
        return self.df.to_dict()

    def get_dataframe_numpy(self):
        return self.df.to_numpy()
