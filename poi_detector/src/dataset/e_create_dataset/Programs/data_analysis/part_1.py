"""
This program reads the csv-database (xml_to_csv of dj-software).
Then for every song it calculates the desired transform and stores its duration in a new csv-file.
"""
from .helpers.part_1_helper import dict_to_csv, read_songs_shapes
from .constants import base_dir
import os

# Variables
transform_type = 'cqt'
window_size = 11.61

# Get list of all songs in the particular dataset
dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))
data_dir = os.path.join(base_dir, 'window_size_' + str(window_size), 'data')
names = os.listdir(data_dir)

# Read every song's spectrogram and store its shape in a dictionary
db = read_songs_shapes(data_dir, names, transform_type, window_size)

# Save the dictionary of shapes in a csv file
dict_to_csv(dataset_dir, db, window_size)
