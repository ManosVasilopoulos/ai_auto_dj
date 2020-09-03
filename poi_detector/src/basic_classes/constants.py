preciser_train_csv_path = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/virtual_dj_17_12_train.csv'
preciser_test_csv_path = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/virtual_dj_17_12_test.csv'
preciser_csv_path = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/virtual_dj_17_12.csv'
relative_locator_csv_path = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/rekordbox_27_3.csv'
relative_locator_train_csv_path = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/rekordbox_27_3_train.csv'
relative_locator_test_csv_path = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/rekordbox_27_3_test.csv'

temp_image_dir = 'D:/Documents/Thesis/Saved Transforms/Temp/'

base_transforms_dir = 'D:/Documents/Thesis/Saved Transforms/Images/'
mels_dir = 'D:/Documents/Thesis/Saved Transforms/Melspectrograms/'
specs_dir = 'D:/Documents/Thesis/Saved Transforms/Spectrograms/'
cqt_dir = 'D:/Documents/Thesis/Saved Transforms/Constant-Qs/'
mfcc_dir = 'D:/Documents/Thesis/Saved Transforms/MFCCs/'

#wav_dir = 'D:/Documents/Thesis/POIs WAV/'
wav_dir = 'D:/Documents/Thesis/WAVs/'

save_directory_gnn = 'D:/Documents/Thesis/Project Skaterbot/POIS Regression/'
project_dir = 'D:/Documents/Thesis/Project Skaterbot/Good Neural Networks/'
trained_cnns_dir = 'D:/Documents/Thesis/Project Skaterbot/Good Neural Networks/Trained CNN/'

pca_dir = 'D:/Documents/Thesis/Project Skaterbot/PCA/'

savepath = 'C:/Users/sk8er/Documents/Python/Thesis/Project Skaterbot/Scripts/Helpful (Not System Files)/TEMP/'

max_minutes = 4
constant = 1
MAX_SAMPLES = int(max_minutes * 60 * 100 // constant)
FIXED_TIME_SAMPLES = int(max_minutes * 60 * 100 // constant)
window_size = 10 * constant  # ms

# Max value calculated
# DATASET_MAX_VALUE = -10.408489
# Normalize with max=-10 instead
#DATASET_MAX_VALUE = -10.0
#DATASET_MIN_VALUE = -140.0

""" ALL BELOW NEED CORRECT VALUES """
MAX_VAL_MELSPEC = -5.0
MIN_VAL_MELSPEC = -100.0

MAX_VAL_SPEC = 0.0
MIN_VAL_SPEC = -100.0

MAX_VAL_MFCC = 0.0
MIN_VAL_MFCC = -4000.0

MAX_VAL_CQT = 0.0
MIN_VAL_CQT = -150.0