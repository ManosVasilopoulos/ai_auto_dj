import numpy as np

from poi_detector.src.basic_classes.architecture import Architecture
from .neural_networks import CNN
from os.path import join as os_path_join


class Preciser(Architecture):
    arch_type = 'Preciser v1'

    def __init__(self, _id, batch_size, time_size, freq_size, transform_type, window_size: float):
        super().__init__(_id, batch_size, time_size, freq_size, transform_type, window_size)
        self.project_dir = self.make_project_dir()

        self.cnn_model, self.metrics_names = self.architecture(time_size, freq_size)
        self.loss = self.cnn_model.loss.__name__
        self.metrics_names = [x.name for x in self.cnn_model.metrics]

    def __get_cnn(self, time_size, freq_size):
        cnn = CNN(self._id)
        return cnn.get_model(time_size, freq_size)

    def architecture(self, time_size, freq_size):
        cnn_model, metrics_names = self.__get_cnn(time_size, freq_size)
        return cnn_model, metrics_names

    def train(self, x, y, epoch):
        history = self.cnn_model.fit(x, y, batch_size=self.batch_size, shuffle=True, epochs=1)

        self.save_train_metrics(history.history, epoch, self.cnn_model.name, self.training_counter)

        self.training_counter += 1
        self.training_samples += x.shape[0]

    def test(self, x, y, epoch):
        history = self.cnn_model.evaluate(x, y, batch_size=self.batch_size)

        self.save_test_metrics(history, epoch, self.cnn_model.name, self.testing_counter,
                               [self.loss] + self.metrics_names)

        self.testing_counter += 1
        self.testing_samples += x.shape[0]

    def train_with_validation(self, x: np.ndarray, y: np.ndarray, validation_data: tuple, epoch: int):
        pass

    def predict(self, x):
        predictions = self.cnn_model.predict(x, batch_size=self.batch_size)

        return predictions

    def save_model(self):
        print("Saving model:", self.cnn_model.name)
        cnn_path = os_path_join(self.project_dir, self.cnn_model.name)
        self.cnn_model.save_weights(cnn_path)

    def load_trained_model(self):
        cnn_path = os_path_join(self.project_dir, self.cnn_model.name)
        self.cnn_model.load_weights(cnn_path)
