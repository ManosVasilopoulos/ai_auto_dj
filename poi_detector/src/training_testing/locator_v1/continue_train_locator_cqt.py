from dataset.load_dataset.data_generator_locator_v1 import SkaterbotDataGenerator
from models.locator_v1.model import Locator1
import os

_id = 3
batch_size = 10
time_size = 100
freq_size = 108
transform_type = 'cqt'
window_size = 11.61

base_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Library\\'
csv_name = 'offsets_list_ts' + str(time_size) + '_mini.csv'

dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))

locator = Locator1(_id, batch_size, time_size, freq_size, transform_type, window_size)
locator.rnn.decoder.summary()
locator.load_trained_model()
my_generator = SkaterbotDataGenerator(dataset_dir, csv_name, time_size, freq_size, window_size, transform_type)

last_epoch = 1
for epoch in range(last_epoch, locator.max_epochs):
    print('-------------------------- Epoch', epoch, '--------------------------')
    for x_train, y_train in my_generator.train_flow_locator_v1(batch_size=10):
        if x_train.shape != (batch_size, my_generator.max_time_steps, my_generator.time_size, my_generator.freq_size):
            print('Skipped_batch')
            continue
        locator.train(x_train, y_train, epoch)

    locator.save_model()

    for x_test, y_test in my_generator.test_flow_locator_v1(batch_size=10):
        if x_test.shape != (batch_size, my_generator.max_time_steps, my_generator.time_size, my_generator.freq_size):
            print('Skipped_batch')
            continue
        locator.test(x_test, y_test, epoch)
    locator.save_log_file(locator.rnn.decoder.name, epoch)
    locator.save_model()
    locator.reset_counters()
