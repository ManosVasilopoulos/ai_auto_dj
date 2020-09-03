from .neural_networks import CNN
import os
_id = 1
model_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Good Neural Networks\\Preciser v1\\'+str(_id)+'\\melspectrogram\\10\\500'
model_txt_path = os.path.join(model_dir, 'model_summary.txt')


def write_to_txt(summary):
    with open(model_txt_path, 'a') as f:
        f.write(summary + '\n')


cnn = CNN(_id)
model, _ = cnn.get_model(500, 256)

model.summary(print_fn=write_to_txt)
