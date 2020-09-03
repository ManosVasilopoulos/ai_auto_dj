from basic_classes.architecture import Architecture
from .input_handler import InputLocatorHandler
from .output_handler import OutputLocatorHandler
from .neural_networks import Encoder, Decoder
import numpy as np


class RelativeLocator(Architecture):

    def __init__(self, encoder_id, decoder_id, batch_size, time_size, freq_size, transform_type, window_size):
        super().__init__(encoder_id, batch_size, time_size, freq_size, transform_type, window_size)
        self.decoder_id = decoder_id
        self.project_dir = self.make_project_dir()

        self.input_handler = InputLocatorHandler(time_size, freq_size, transform_type, window_size)
        self.output_handler = OutputLocatorHandler(time_size, window_size)
        self.encoder, self.decoder, self.metrics_names = self.architecture(time_size, freq_size)

    def __predict_features(self, spec_batch):
        predicted_feats_batch = []
        for x in spec_batch:
            predicted_feats_batch.append(self.decoder.predict(x, batch_size=1))
        return np.array(predicted_feats_batch)

    def train(self, x, y, epoch):
        x_features = self.__predict_features(x)

    def test(self, x, y, epoch):
        pass

    def predict(self, x):
        pass

    def architecture(self, time_size, freq_size):
        encoder = Encoder(self._id).get_model(time_size, freq_size)
        encoder_output_size = encoder.output_shape[1]
        decoder, metrics_names = Decoder(self.decoder_id).get_model(time_size, encoder_output_size)
        return encoder, decoder, metrics_names

    def save_model(self):
        pass

    def load_trained_model(self):
        pass

    def make_project_dir(self):
        new_project_dir = self.project_dir + 'Relative Locator/'
        new_project_dir += str(self._id) + '/'
        new_project_dir += str(self.transform_type) + '/'
        new_project_dir += str(self.time_size) + '/'
        return new_project_dir
