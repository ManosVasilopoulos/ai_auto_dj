from basic_classes.architecture import Architecture
from .input_handler import InputPCALocatorHandler
from .output_handler import OutputPCALocatorHandler
from .neural_networks import LSTMDecoder
import pickle
import numpy as np


class PCALocator(Architecture):
    pca_path = 'D:/Documents/Thesis/Project Skaterbot/PCA/spectrogram_pca29_3.sav'

    def __init__(self, _id, batch_size, time_size, freq_size, transform_type, window_size):
        super().__init__(_id, batch_size, time_size, freq_size, transform_type, window_size)
        self.project_dir = self.make_project_dir()

        self.input_handler = InputPCALocatorHandler(time_size, freq_size, transform_type, window_size)
        self.output_handler = OutputPCALocatorHandler(time_size, window_size)
        self.pca_transformer, self.lstm_model, self.metrics_names = self.architecture(time_size, freq_size)

    def __predict_features(self, x):
        batch = []
        for i, sample in enumerate(x):
            predictions = self.pca_transformer.transform(sample)
            batch.append(predictions)
        return np.array(batch)

    def __get_pca_encoder(self):
        with open(self.pca_path, 'rb') as file:
            pca_transformer = pickle.load(file)

        return pca_transformer

    def __get_lstm_decoder(self, time_size, freq_size):
        lstm_decoder = LSTMDecoder(self._id)
        return lstm_decoder.get_model(time_size, freq_size)

    def architecture(self, time_size, freq_size):
        pca_transformer = self.__get_pca_encoder()
        lstm_model, metrics_names = self.__get_lstm_decoder(time_size, freq_size)
        return pca_transformer, lstm_model, metrics_names

    def train(self, x, y, epoch):
        x_features = self.__predict_features(x)

        history = self.lstm_model.fit(x_features, y, shuffle=True, epochs=1)

        self.save_metrics(history.history, epoch, self.lstm_model.name, self.training_counter, self.metrics_names)

        self.training_counter += 1
        self.training_samples += x_features.shape[0]

    def test(self, x, y, epoch):
        x_features = self.__predict_features(x)

        history = self.lstm_model.evaluate(x_features, y, batch_size=1)

        self.save_metrics(history, epoch, self.lstm_model.name, self.testing_counter, self.metrics_names)

        self.testing_counter += 1
        self.testing_samples += x_features.shape[0]

    def predict(self, x):
        x_features = self.__predict_features(x)

        predictions = self.lstm_model.predict(x_features, batch_size=1)

        return predictions

    def save_model(self, epoch):
        print("SAVING MODEL's WEIGHTS...")
        self.lstm_model.save_weights(self.project_dir + self.lstm_model.name)

    def load_trained_model(self, model_name):
        self.load_log_file()
        self.lstm_model.load_weights(self.project_dir + model_name)

    def make_project_dir(self):
        new_project_dir = self.project_dir + 'PCA Locator/'
        new_project_dir += str(self._id) + '/'
        new_project_dir += str(self.transform_type) + '/'
        new_project_dir += str(self.time_size) + '/'
        return new_project_dir
