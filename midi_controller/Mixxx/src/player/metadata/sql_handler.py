import sqlite3
from os.path import join as ospathjoin
import numpy as np


class SQLHandler:
    db_dir = 'C:\\Users\\sk8er\\AppData\\Local\\Mixxx\\'

    def __init__(self):
        conn = sqlite3.connect(ospathjoin(self.db_dir, 'mixxxdb.sqlite'))
        self.cur = conn.cursor()

    # Tested - OK
    def store_all_tables_names(self, playlists_dir: str):
        tables_names = self.get_all_tables_name()
        with open(ospathjoin(playlists_dir, 'tables_names.txt'), 'w+') as f:
            f.writelines(tables_names)

    # Tested - OK
    def get_all_tables_name(self):
        response = self.cur.execute('select name from sqlite_master')

        tables_names = []
        for name in response:
            if type(name) == tuple or type(name) == list:
                tables_names.append(name[0] + '\n')
            else:
                tables_names.append(name + '\n')
        return tables_names

    # Tested - OK
    def store_table_fields(self, table_name: str, playlists_dir: str):
        response = self.cur.execute('select * from ' + table_name)
        fields_names = [description[0] + '\n' for description in response.description]
        with open(ospathjoin(playlists_dir, table_name + '.txt'), 'w+') as f:
            f.writelines(fields_names)

    # Tested - OK
    def print_fields_of_table(self, table_name: str):
        response = self.cur.execute('select * from ' + table_name)
        fields_names = [description[0] for description in response.description]
        for name in fields_names:
            print(name)

    # Tested - OK
    def get_library_records(self):
        response = self.cur.execute('select id, title, bpm, key from library')
        records = {}
        for record in response:
            records[record[1]] = record

        return np.array(records)

    # Tested - OK
    def get_playlists(self):
        response = self.cur.execute('select id, name from Playlists')

        records = {}
        for record in response:
            records[record[1]] = record

        return records

    # Tested - OK
    def get_playlist_tracks(self, playlist_name: str):
        playlist_id = self.get_playlist_id(playlist_name)
        response = self.cur.execute('select track_id from PlaylistTracks where playlist_id=:playlist_id',
                                    {"playlist_id": str(playlist_id)})

        records = []
        for record in response:
            records.append(record[0])

        return records

    # Tested - OK
    def get_playlist_id(self, playlist_name: str):
        """ It is assumed that 'name' has UNIQUE values"""
        response = self.cur.execute("select id from Playlists where name=:playlist_name",
                                    {"playlist_name": playlist_name})

        for tup in response:
            return tup[0]
    def get_track_id(self, track_name: str):
        """ It is assumed that 'name' has UNIQUE values"""
        response = self.cur.execute("select id from library where name=:track_name",
                                    {"track_name": track_name})

        for tup in response:
            return tup[0]

    # Tested - OK
    def get_track_metadata(self, track_id: int):
        filename = self.get_track_name(track_id)
        response = self.cur.execute("select location, bpm, key, duration from library where id=:track_id",
                                    {"track_id": str(track_id)})
        metadata = {}
        for tup in response:
            metadata[filename] = {"bpm": tup[1], "key": tup[2], "duration": tup[3]}
        return metadata

    def get_track_all_metadata(self, track_id: int):
        response = self.cur.execute("select * from library where id=:track_id",
                                    {"track_id": str(track_id)})

        metadata = {}
        for tup in response:
            metadata[tup[0]] = tup
        return metadata

    def get_track_name(self, track_id: int):
        response = self.cur.execute("select filename from track_locations where id=:track_id",
                                    {"track_id": str(track_id)})
        for tup in response:
            return tup[0]

    def get_playlist_tracks_metadata(self, playlist_name: str):
        track_ids = self.get_playlist_tracks(playlist_name)
        tracks_metadata = {}
        for track_id in track_ids:
            track_metadata = self.get_track_metadata(track_id)
            for track_name in track_metadata:
                tracks_metadata[track_name] = track_metadata[track_name]
        return tracks_metadata
