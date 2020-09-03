import pandas as pd


def get_transform_shapes(csv_path: str):
    df = pd.read_csv(csv_path)
    spec_shapes_numpy = df.to_numpy()
    new_dict = {}
    for i, name in enumerate(spec_shapes_numpy):
        x = (name[1], name[2])
        new_dict[name[0]] = x
    return new_dict
