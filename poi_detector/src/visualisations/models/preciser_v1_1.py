from models.preciser_v1.neural_networks import CNN
from os.path import join

path = 'D:\Documents\Thesis\THESIS CHAPTERS\Chapter 7 Images\Preciser V1'
_id = 1
cnn = CNN(_id)



model, _ = cnn.get_model(500, 256)
model.summary()
