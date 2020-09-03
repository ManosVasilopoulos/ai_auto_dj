from poi_detector.src.basic_classes.constants import relative_locator_train_csv_path
from poi_detector.src.basic_classes.constants import relative_locator_test_csv_path
from poi_detector.src.basic_classes.constants import relative_locator_csv_path

fid = open(relative_locator_csv_path, "r")
li = fid.readlines()
fid.close()

n_samples = len(li)

n_songs = n_samples // 7

n_train = int(0.8*n_songs) * 7
n_test = n_samples - n_train

fid = open(relative_locator_train_csv_path, 'w')
fid.writelines(li[:n_train])
fid.close()

fid = open(relative_locator_test_csv_path, 'w')
fid.writelines(li[n_train:])
fid.close()
