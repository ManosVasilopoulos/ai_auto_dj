from tensorflow import keras
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
from basic_classes import constants
from basic_classes.neural_networks import NN


class LSTMDecoder(NN):

    def get_model(self, time_size, freq_size):
        if self._id == 1:
            return self.__decoder1(time_size, freq_size)
        else:
            raise Exception(
                'LSTMDecoder: lstm-decoder with id higher or equal to "' + str(self._id) + '" does not exist.')

    @staticmethod
    def __decoder1(time_size, freq_size):
        timesteps = constants.MAX_SAMPLES // time_size
        n_features = freq_size  # same value as the output layer of encoder

        # Architecture
        input_rnn = keras.layers.Input(shape=(timesteps, n_features), name='Decoder_Input')
        lstm = CuDNNLSTM(units=50, return_sequences=True, name='LSTM_1')(input_rnn)
        flat = keras.layers.Flatten(name='Flattener')(lstm)
        dense = keras.layers.Dense(256, name='Dense_1', activation='relu')(flat)
        output_rnn = keras.layers.Dense(timesteps, activation='sigmoid', name='Decoder_Output_Dense')(dense)

        model = keras.Model(name='LSTM-PCA-1', inputs=input_rnn, outputs=output_rnn)

        loss = keras.losses.binary_crossentropy
        accuracy = keras.metrics.binary_accuracy
        optimiser = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

        metrics_names = [loss.__name__, accuracy.__name__]

        model.compile(optimizer=optimiser, loss=loss, metrics=[loss, accuracy])
        return model, metrics_names
