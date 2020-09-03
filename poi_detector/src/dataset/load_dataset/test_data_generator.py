from .data_generator import SkaterbotDataGenerator

dataset_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Datasets\\Relative Locator\\spectrogram\\window_size_100\\time_size_1000\\'
csv_name = 'offsets_list_dataset.csv'
my_generator = SkaterbotDataGenerator(dataset_dir, csv_name, 1000, 4411, 100)

for x_test, y_test in my_generator.test_flow(1, False):
    print(x_test.shape, y_test.shape)
    print("%d bytes" % (x_test.size * x_test.itemsize))
