import numpy as np
from sklearn.decomposition import IncrementalPCA
from basic_classes.helper import get_data_from_csv
from basic_classes.get_input import Input
from basic_classes.constants import preciser_csv_path, pca_dir
from datetime import datetime
import joblib

# Create and save model
dt = datetime.now()
current_day = str(dt.day)
current_month = str(dt.month)
pca_transformer = IncrementalPCA(n_components=512, batch_size=100)
filename = 'pca' + str(current_day) + '_' + str(current_month) + '.joblib'
joblib.dump(pca_transformer, pca_dir + filename)

""" Get Input-names """
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
        for j in range(x_s.shape[0]):
            x_train.append(x_s[j])
        if len(x_train) < 512:
            continue
        x_train = np.array(x_train)
        print('Fitting data to PCA model: ' + str(x_train.shape))
        pca_transformer.partial_fit(X=x_train)
        print('Used: ' + str(i+1) + ' out of ' + str(n_samples))
        x_train = []
    except Exception as e:
        print(e)
        continue
    print('SAVING...')
    joblib.dump(pca_transformer, pca_dir + filename)
