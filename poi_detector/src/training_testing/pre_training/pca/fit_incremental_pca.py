from os.path import join as pathjoin
from .helper import mk_pca_dir, transform_ims_to_vecs
from dataset.load_dataset.data_generator import SkaterbotDataGenerator
from sklearn.decomposition import IncrementalPCA
from joblib import dump, load

""" constants """
window_size = 11.61
time_size = 100
freq_size = 108
transform_type = 'cqt'

project_dir = 'D:\\Documents\\Thesis\\Project Skaterbot'
library_dir = pathjoin(project_dir, 'Datasets', 'Library')
dataset_dir = pathjoin(library_dir, 'window_size_' + str(window_size))
print('Dataset Directory:', dataset_dir)

""" PCA Configuration """
in_length = time_size * freq_size
out_length = int(in_length / 20)
pca_dir = pathjoin(project_dir, 'PCA')
print('Directory:', pca_dir)
print('PCA "input vector length":', in_length, '"output vector length":', out_length)
ipca = IncrementalPCA(n_components=out_length, batch_size=out_length)

pca_model_dir = mk_pca_dir(pca_dir, transform_type, window_size, time_size, freq_size)
pca_path = pathjoin(pca_model_dir, 'pca_cqt.joblib')
print('PCA Model Path:', pca_path)

""" DATASET """
csv_name = 'offsets_list_ts' + str(time_size) + '.csv'

# Inititialize Data Generator
my_generator = SkaterbotDataGenerator(dataset_dir, csv_name, time_size, freq_size, window_size, transform_type)
n_samples = my_generator.n_samples

i = 0
for x_train in my_generator.input_flow(batch_size=out_length):
    x_train = transform_ims_to_vecs(x_train)
    ipca.partial_fit(X=x_train)
    print('Finished:', my_generator.train_counter, 'out of', n_samples)
    i += 1

    if i % 100 == 0:
        dump(ipca, pca_path)
        print('Saved PCA model')


dump(ipca, pca_path)
