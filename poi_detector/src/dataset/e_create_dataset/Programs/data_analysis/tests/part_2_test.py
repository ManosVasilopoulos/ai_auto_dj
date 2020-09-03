from ..helpers.part_2_helper import csv_to_numpy
import os
from ..constants import base_dir

dataset_dir = os.path.join(base_dir, 'window_size_100')

csv_name = 'spec_shapes_ws_100.csv'
csv_path = os.path.join(dataset_dir, csv_name)

dict_ = csv_to_numpy(csv_path)

for name in dict_:
    print(name)
