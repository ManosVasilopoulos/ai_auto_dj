from basic_classes.architecture import Architecture
from .input_handler import InputPreciserHandler
from .output_handler import OutputPreciserHandler
from .neural_networks import CNN
from .dataset_balancer import PreciserBalancer

class Preciser(Architecture):

    def __init__(self, _id, batch_size, time_size, freq_size, transform_type, window_size):
        super().__init__(_id, batch_size, time_size, freq_size, transform_type, window_size)
        self.project_dir = self.make_project_dir()

        self.input_handler = InputPreciserHandler(time_size, freq_size, transform_type, window_size)
        self.output_handler = OutputPreciserHandler(time_size, window_size)
        self.input_output_handler = PreciserBalancer(self.input_handler, self.output_handler, time_size, freq_size)
        self.cnn_model, self.metrics_names = self.architecture(time_size, freq_size)

    def __get_cnn(self, time_size, freq_size):
        cnn = CNN(self._id)
        return cnn.get_model(time_size, freq_size)

    def architecture(self, time_size, freq_size):
        cnn_model, metrics_names = self.__get_cnn(time_size, freq_size)
        return cnn_model, metrics_names

    def train(self, x, y, epoch):
        history = self.cnn_model.fit(x, y, batch_size=self.batch_size, shuffle=True, epochs=1)

        self.save_train_metrics(history.history, epoch, self.cnn_model.name, self.training_counter, self.metrics_names)

        self.training_counter += 1
        self.training_samples += x.shape[0]

    def test(self, x, y, epoch):
        history = self.cnn_model.evaluate(x, y, batch_size=self.batch_size)

        self.save_test_metrics(history, epoch, self.cnn_model.name, self.testing_counter, self.metrics_names)

        self.testing_counter += 1
        self.testing_samples += x.shape[0]

    def predict(self, x):
        predictions = self.cnn_model.predict(x, batch_size=self.batch_size)

        return predictions

    def save_model(self):
        print("Saving model:", self.cnn_model.name)
        self.cnn_model.save_weights(self.project_dir + self.cnn_model.name)

    def load_trained_model(self):
        self.load_log_file()
        self.cnn_model.load_weights(self.project_dir + self.cnn_model.name)

    def make_project_dir(self):
        new_project_dir = self.project_dir + 'Preciser v3/'
        new_project_dir += str(self._id) + '/'
        new_project_dir += str(self.transform_type) + '/'
        new_project_dir += str(self.window_size) + '/'
        new_project_dir += str(self.time_size) + '/'
        return new_project_dir
