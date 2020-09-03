from dataset.load_dataset.data_generator2 import SkaterbotDataGenerator
from models.locator_v2.model import Locator2
import os

base_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Library\\'
csv_name = 'offsets_list_dataset.csv'

_id = 7
batch_size = 4
time_size = 1000
freq_size = 256
transform_type = 'melspectrogram'
window_size = 100

dataset_dir = os.path.join(base_dir, 'window_size_' + str(window_size))

locator = Locator2(_id, batch_size, time_size, freq_size, transform_type, window_size)
locator.cnn_model.summary()
my_generator = SkaterbotDataGenerator(dataset_dir, csv_name,
                                      time_size, freq_size, window_size, transform_type,
                                      train_test_ratio=0.8,
                                      distribution_mode=True)

for epoch in range(locator.max_epochs):
    print('-------------------------- Epoch', epoch, '--------------------------')
    for train_data, validation_data in zip(my_generator.train_flow(batch_size * 5),
                                           my_generator.validation_flow(batch_size)):
        x_train, y_train = train_data
        x_validation, y_validation = validation_data
        if x_train.shape != (batch_size * 5, time_size, freq_size, 1):
            print('Skipped this training turn. x_train.shape:', x_train.shape)
            break
        if y_train.shape != (batch_size * 5, time_size):
            print('Skipped this training turn. y_train.shape:', y_train.shape)
            break
        locator.train_with_validation(x_train, y_train, (x_validation, y_validation), epoch)

    locator.save_model()

    for x_test, y_test in my_generator.test_flow(batch_size=batch_size * 5):
        if x_test.shape != (batch_size * 5, time_size, freq_size, 1):
            print('Skipped this testing turn. x_test.shape:', x_test.shape)
            break
        if y_test.shape != (batch_size * 5, time_size):
            print('Skipped this testing turn. y_test.shape:', y_test.shape)
            break
        locator.test(x_test, y_test, epoch)
    locator.save_log_file(locator.cnn_model.name, epoch)
    locator.save_model()
    locator.reset_counters()
