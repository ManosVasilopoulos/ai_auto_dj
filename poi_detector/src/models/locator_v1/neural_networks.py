from tensorflow import keras
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
from .feature_extractors import FeatureExtractorCNN, FeatureExtractorPCA, FeatureExtractor


class RNN:
    feature_extractor: FeatureExtractor
    decoder: keras.Model

    max_seconds = 100  # Locator v2 uses inputs that last 100 seconds as well.

    metrics_names: list

    def __init__(self, _id: int, transform_type: str, window_size: float, time_size: int, freq_size: int):
        self._id = _id
        self.initialize_model(transform_type, window_size, time_size, freq_size)

    def __calculate_timesteps(self, time_size, window_size):
        time_steps = int(self.max_seconds * (1000 / window_size) / time_size)
        return time_steps

    def initialize_model(self, transform_type: str, window_size: float, time_size: int, freq_size: int):
        time_steps = self.__calculate_timesteps(time_size, window_size)
        if self._id == 1:
            self.feature_extractor, n_feats = FeatureExtractorCNN().load_feature_extractor(7, transform_type,
                                                                                           window_size,
                                                                                           time_size, freq_size,
                                                                                           'dense_features_1')
            self.decoder, self.metrics_names = self.__rnn1(time_steps, n_feats)
        elif self._id == 2:
            self.feature_extractor = FeatureExtractorCNN()
            _, n_feats = self.feature_extractor.load_feature_extractor(7, transform_type,
                                                                       window_size,
                                                                       time_size, freq_size,
                                                                       'dense_features_1')
            self.decoder, self.metrics_names = self.__rnn2(time_steps, n_feats)
            return self.__rnn2(time_steps, n_feats)
        elif self._id == 3:
            self.feature_extractor = FeatureExtractorPCA()

            _, n_feats = self.feature_extractor.load_feature_extractor(transform_type, window_size,
                                                                       time_size, freq_size)
            self.decoder, self.metrics_names = self.__rnn1(time_steps, n_feats)
        elif self._id == 4:
            self.feature_extractor = FeatureExtractorPCA()
            _, n_feats = self.feature_extractor.load_feature_extractor(transform_type, window_size,
                                                                       time_size, freq_size)
            self.decoder, self.metrics_names = self.__rnn2(time_steps, n_feats)
        else:
            raise Exception(
                'RNNError: rnn with id higher or equal to "' + str(self._id) + '" does not exist.')

    def __rnn1(self, timesteps: int, n_feats: int):
        """ Feature Extractor """

        """ RNN """
        input_rnn = keras.layers.Input(shape=(timesteps, n_feats), name='locator-1_input')

        lstm = CuDNNLSTM(units=100, return_sequences=True, name='lstm')(input_rnn)

        flat = keras.layers.Flatten(name='flat')(lstm)

        # ------------------------------------------
        dense = keras.layers.Dense(1024)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        output_rnn = keras.layers.Dense(timesteps, activation='sigmoid', name='locator-1_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_rnn, outputs=output_rnn, name='Locator_v1-1')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    def __rnn2(self, timesteps: int, n_feats: int):
        """ Feature Extractor """

        """ RNN """
        input_rnn = keras.layers.Input(shape=(timesteps, n_feats), name='locator-2_input')

        lstm = CuDNNLSTM(units=500, name='lstm')(input_rnn)
        flat = keras.layers.Flatten(name='flat')(lstm)

        # ------------------------------------------
        dense = keras.layers.Dense(1024)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        output_rnn = keras.layers.Dense(timesteps, activation='sigmoid', name='locator-2_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_rnn, outputs=output_rnn, name='Locator_v1-2')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names
