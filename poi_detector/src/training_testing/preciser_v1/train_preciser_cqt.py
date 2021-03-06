from dataset.load_dataset.data_generator import SkaterbotDataGenerator
from models.preciser_v1.model import Preciser
import os
import skimage.io

base_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Library\\'
temp_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Temp_CQT'

""" DATASET """
_id = 8
batch_size = 32
time_size = 100
freq_size = 108
transform_type = 'cqt'
window_size = 11.61

""" DATASET """
csv_name = 'offsets_list_ts' + str(time_size) + '.csv'

dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))

preciser = Preciser(_id, batch_size, time_size, freq_size, transform_type, window_size)
preciser.cnn_model.summary()
my_generator = SkaterbotDataGenerator(dataset_dir, csv_name, time_size, freq_size, window_size, transform_type)
samples_used = 0

for epoch in range(preciser.max_epochs):
    print('-------------------------- Epoch', epoch, '--------------------------')
    for x_train, y_train in my_generator.train_flow(batch_size=100, regression_mode=True):
        """
        for i, x in enumerate(x_train):
            skimage.io.imsave(os.path.join(temp_dir, str(samples_used) + '.jpg'), x)
            samples_used += 1
        """
        preciser.train(x_train, y_train, epoch)

    preciser.save_model()

    for x_test, y_test in my_generator.test_flow(batch_size=100, regression_mode=True):
        preciser.test(x_test, y_test, epoch)
    preciser.save_log_file(preciser.cnn_model.name, epoch)
    preciser.save_model()
    preciser.reset_counters()
