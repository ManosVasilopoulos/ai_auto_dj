import numpy as np
from basic_classes.architecture import Architecture
from .input_handler import InputLocatorHandler2
from .output_handler import OutputLocatorHandler2
from .data_balancer import LocatorBalancer2
from .neural_networks import CNN


class RelativeLocator2(Architecture):
    model_type = 'Relative Locator v2'

    def __init__(self, _id, batch_size, time_size, freq_size, transform_type, window_size):
        self.__check_values(time_size, window_size)

        super().__init__(_id, batch_size, time_size, freq_size, transform_type, window_size)

        self.project_dir = self.make_project_dir()
        self.input_handler = InputLocatorHandler2(time_size, freq_size, transform_type, window_size)
        self.output_handler = OutputLocatorHandler2(time_size, window_size)
        self.input_output_handler = LocatorBalancer2(time_size, freq_size, window_size)
        self.cnn_model, self.metrics_names = self.architecture(time_size, freq_size)

    def train(self, x: np.ndarray, y: np.ndarray, epoch: int):
        history = self.cnn_model.fit(x, y, batch_size=self.batch_size, shuffle=True, epochs=1)

        self.save_train_metrics(history.history, epoch, self.cnn_model.name, self.training_counter, self.metrics_names)

        self.training_counter += 1
        self.training_samples += x.shape[0]

    def test(self, x: np.ndarray, y: np.ndarray, epoch: int):
        history = self.cnn_model.evaluate(x, y, batch_size=self.batch_size)

        self.save_test_metrics(history, epoch, self.cnn_model.name, self.testing_counter, self.metrics_names)

        self.testing_counter += 1
        self.testing_samples += x.shape[0]

    def predict(self, x: np.ndarray):
        predictions = self.cnn_model.predict(x, batch_size=self.batch_size)

        return predictions

    def architecture(self, time_size: int, freq_size: int):
        cnn = CNN(self._id)
        return cnn.get_model(time_size, freq_size)

    def save_model(self):
        print("Saving model:", self.cnn_model.name)
        self.cnn_model.save_weights(self.project_dir + self.cnn_model.name)

    def load_trained_model(self):
        self.load_log_file()
        self.cnn_model.load_weights(self.project_dir + self.cnn_model.name)

    def make_project_dir(self):
        new_project_dir = self.project_dir + self.model_type + '/'
        new_project_dir += str(self._id) + '/'
        new_project_dir += str(self.transform_type) + '/'
        new_project_dir += str(self.window_size) + '/'
        return new_project_dir

    def __check_values(self, ts: int, ws: int):
        if ts < 1000:
            raise Exception('RelativeLocator model.py ERROR: time_size must have a value greater than 1000.')
        if ws < 50:
            raise Exception('RelativeLocator model.py ERROR: window_size must have a value greater than 50.')
