from dataset.load_dataset.data_generator import SkaterbotDataGenerator
from models.preciser_v1.model import Preciser
import os

epoch = int(input('Enter the last epoch of the previous training: ')) + 1


base_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Library\\'
temp_dir = 'D:\\Documents\\Thesis\\Saved Transforms\\'
_id = 7
batch_size = 8
time_size = 500
freq_size = 512
transform_type = 'spectrogram'
window_size = 10
csv_name = 'offsets_list_ts' + str(time_size) + '_mini.csv'

dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))

preciser = Preciser(_id, batch_size, time_size, freq_size, transform_type, window_size)
preciser.cnn_model.summary()
preciser.load_trained_model()

my_generator = SkaterbotDataGenerator(dataset_dir, csv_name, time_size, freq_size, window_size, transform_type)

for epoch in range(epoch, preciser.max_epochs):
    print('-------------------------- Epoch', epoch, '--------------------------')
    for x_train, y_train in my_generator.train_flow(batch_size=100, regression_mode=True):

        preciser.train(x_train, y_train, epoch)

    preciser.save_model()

    for x_test, y_test in my_generator.test_flow(batch_size=100, regression_mode=True):
        preciser.test(x_test, y_test, epoch)
    preciser.save_log_file(preciser.cnn_model.name, epoch)
    preciser.save_model()
    preciser.reset_counters()
