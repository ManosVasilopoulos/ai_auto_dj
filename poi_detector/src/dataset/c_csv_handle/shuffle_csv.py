import random
from poi_detector.src.basic_classes.constants import relative_locator_train_csv_path

fid = open(relative_locator_train_csv_path, "r")
lines = fid.readlines()
fid.close()

new_lines = []
for line in lines:
    if line != '\n':
        new_lines.append(line)

random.shuffle(new_lines)

fid = open(relative_locator_train_csv_path, "w")
fid.writelines(new_lines)
fid.close()
