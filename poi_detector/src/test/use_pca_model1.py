import numpy as np
from sklearn.decomposition import IncrementalPCA
from basic_classes.helper import get_data_from_csv
from basic_classes.get_input import Input
from basic_classes.constants import preciser_csv_path, pca_dir
import pickle
from datetime import datetime
import joblib
import sys

# LOAD PCA MODEL
filename = 'pca19_3.joblib'
pca_transformer = joblib.load(pca_dir + filename)
print(pca_transformer)
""" Get Input-names and Output-Points of Interest """
# the last csv that is used has all songs shuffled. No need to process input names.
input_names, output_pois = get_data_from_csv(preciser_csv_path)

n_samples = input_names.shape[0]

n_train = n_samples

input_names = input_names[:n_train]

in_obj = Input('PCA', 500, 512, 'melspectrogram')

x_train = []
batch_count = 0
for i in range(n_train):
    sample_name = input_names[i]
    print('\n==========================================================================')
    print("Reading: " + sample_name)
    try:
        """---------------------GET INPUT------------------------------------------------------------------------"""
        x_s, last_subspec_id = in_obj.read_input(sample_name)
        x_s = in_obj.normalize_input(x_s)
        print(x_s.shape)
        feats_list = pca_transformer.transform(x_s)
        print(feats_list.shape)
        break
        x_train = []
    except Exception as e:
        print(e)
        continue


