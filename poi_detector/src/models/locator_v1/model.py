from poi_detector.src.basic_classes.architecture import Architecture
from .neural_networks import RNN
from os.path import join as os_path_join
import numpy as np


class Locator1(Architecture):
    rnn: RNN
    arch_type = 'Relative Locator v1'

    def __init__(self, _id, batch_size, time_size, freq_size, transform_type, window_size):
        super().__init__(_id, batch_size, time_size, freq_size, transform_type, window_size)
        self.project_dir = self.make_project_dir()

        self.rnn = self.__get_rnn(transform_type, window_size, time_size, freq_size)
        self.loss = self.rnn.decoder.loss.__name__
        self.metrics_names = [x.name for x in self.rnn.decoder.metrics]

    def __get_rnn(self, transform_type: str, window_size: float, time_size, freq_size):
        return RNN(self._id, transform_type, window_size, time_size, freq_size)

    def architecture(self, time_size, freq_size):
        pass

    def train(self, x_batch, y_batch, epoch):
        x_feats_batch = self.rnn.feature_extractor.extract_batch_features(x_batch)

        history = self.rnn.decoder.fit(x_feats_batch, y_batch, batch_size=self.batch_size, shuffle=True, epochs=1)

        self.save_train_metrics(history.history, epoch, self.rnn.decoder.name, self.training_counter)

        self.training_counter += 1
        self.training_samples += x_batch.shape[0]

    def train_with_validation(self, x, y, validation_data: tuple, epoch: int):
        x_feats_batch = self.rnn.feature_extractor.extract_batch_features(x)

        history = self.rnn.decoder.fit(x_feats_batch, y, validation_data=validation_data,
                                       batch_size=self.batch_size, shuffle=True, epochs=1)

        self.save_train_metrics(history.history, epoch, self.rnn.decoder.name, self.training_counter)

        self.training_counter += 1
        self.training_samples += x.shape[0]

        self.validation_counter += 1
        self.validation_samples += validation_data[0].shape[0]

    def test(self, x_batch, y_batch, epoch):
        x_feats_batch = self.rnn.feature_extractor.extract_batch_features(x_batch)
        history = self.rnn.decoder.evaluate(x_feats_batch, y_batch, batch_size=self.batch_size)

        self.save_test_metrics(history, epoch, self.rnn.decoder.name, self.testing_counter, [self.loss] + self.metrics_names)

        self.testing_counter += 1
        self.testing_samples += x_batch.shape[0]

    def predict(self, x_s):
        x_feats_batch = []
        for x in x_s:
            x_feats = self.rnn.feature_extractor.extract_features(x)
            x_feats_batch.append(x_feats)
        x_feats_batch = np.array(x_feats_batch)
        predictions = self.rnn.decoder.predict(x_feats_batch, batch_size=self.batch_size)

        return predictions

    def save_model(self):
        print("Saving model:", self.rnn.decoder.name)
        model_path = os_path_join(self.project_dir, self.rnn.decoder.name)
        self.rnn.decoder.save_weights(model_path)

    def load_trained_model(self):
        model_path = os_path_join(self.project_dir, self.rnn.decoder.name)
        self.rnn.decoder.load_weights(model_path)
