import pandas as pd
import os
from poi_detector.src.dataset.create_dataset.Classes.input_handler import InputDatasetHandler


def read_songs_shapes(data_dir: str, names: list, transform_type: str, window_size: float):
    n_samples = len(names)
    input_handler = InputDatasetHandler(transform_type, window_size)

    db = {}
    for i, name in enumerate(names):
        try:
            file_dir = os.path.join(data_dir, name)
            full_transform = input_handler.read_input_npy(file_dir, name+transform_type)
            db[name] = full_transform.shape
            print('Finished', i + 1, 'out of', n_samples)
            if i % 100 == 0:
                os.system('cls')
        except Exception as e:
            print(e)
            continue
    return db

def dict_to_csv(dataset_dir: str, db: dict, window_size: float):
    df = pd.DataFrame.from_dict(db, orient="index")

    try:
        os.mkdir(dataset_dir)
    except:
        pass

    csv_name = 'spec_shapes_ws_' + str(window_size) + '.csv'
    csv_path = os.path.join(dataset_dir, csv_name)
    df.to_csv(csv_path)
