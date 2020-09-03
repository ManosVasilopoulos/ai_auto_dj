import pandas as pd
import numpy as np

def load_dataset(csv_path: str, train_test_ratio: float, shuffle=True):
    df = pd.read_csv(csv_path)
    dataset = df.to_numpy()[:, 1]

    n_samples = dataset.shape[0]
    n_train = int(train_test_ratio*n_samples)
    trainset = dataset[:n_train]
    if shuffle:
        np.random.shuffle(trainset)
    testset = dataset[n_train:n_samples]

    return trainset, testset


