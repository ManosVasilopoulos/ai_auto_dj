from tensorflow import keras
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
from basic_classes import constants
from basic_classes.neural_networks import NN


class Decoder(NN):

    def get_model(self, time_size, freq_size):
        if self._id == 1:
            return self.__decoder1(time_size, freq_size)
        if self._id == 2:
            return self.__decoder2(time_size, freq_size)
        else:
            raise Exception('Decoder: decoder with id="' + str(self._id) + '" has not been implemented yet.')

    def __decoder1(self, time_size, freq_size):
        timesteps = constants.MAX_SAMPLES // time_size
        n_features = freq_size  # same value as the output layer of encoder

        decoder_in = keras.layers.Input(shape=(timesteps, n_features), name='Decoder_Input')

        lstm = CuDNNLSTM(units=128, return_sequences=True, name='lstm')(decoder_in)

        flat = keras.layers.Flatten(name='rnn_flat')(lstm)

        dense1 = keras.layers.Dense(512, name='rnn_dense_1')(flat)
        leaky1 = keras.layers.LeakyReLU(name='rnn_leaky_1')(dense1)

        decoder_out = keras.layers.Dense(timesteps, activation='sigmoid', name='dense_dec_out')(leaky1)

        model = keras.Model(name='TrainedCNN_with_GRU', inputs=decoder_in, outputs=decoder_out)

        loss = keras.losses.binary_crossentropy
        accuracy = keras.metrics.binary_accuracy
        optimiser = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

        model.compile(optimizer=optimiser, loss=loss, metrics=[accuracy])

        metrics_names = [loss.__name__, accuracy.__name__]
        return model, metrics_names

    def __decoder2(self, time_size, freq_size):
        timesteps = constants.MAX_SAMPLES // time_size
        n_features = freq_size  # same value as the output layer of encoder

        decoder_in = keras.layers.Input(shape=(timesteps, n_features), name='Decoder_Input')
        lstm = CuDNNLSTM(units=256, return_sequences=True, name='lstm1')(decoder_in)
        lstm = CuDNNLSTM(units=128, return_sequences=True, name='lstm2')(lstm)
        flat = keras.layers.Flatten(name='rnn_flat')(lstm)
        dense1 = keras.layers.Dense(1028, name='rnn_dense_1')(flat)
        leaky1 = keras.layers.LeakyReLU(name='rnn_leaky_1')(dense1)
        decoder_out = keras.layers.Dense(timesteps, activation='sigmoid', name='dense_dec_out')(leaky1)
        model = keras.Model(name='TrainedCNN_with_GRU', inputs=decoder_in, outputs=decoder_out)
        loss = keras.losses.binary_crossentropy
        accuracy = keras.metrics.binary_accuracy
        optimiser = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=optimiser, loss=loss, metrics=[accuracy])

        metrics_names = [loss.__name__, accuracy.__name__]

        return model, metrics_names


class Encoder(NN):

    def get_model(self, time_size, freq_size):
        if self._id == 1:
            return self.__encoder1(time_size, freq_size)
        else:
            raise Exception('Decoder: decoder with id="' + str(self._id) + '" has not been implemented yet.')

    def __encoder1(self, time_size, freq_size):

        if time_size != 500 or freq_size != 512:
            raise Exception("EncoderError: encoder-1's input shape is strictly (t, f, n_ch) = (500, 512, 1)")

        def trained_cnn1(trained_encoder_path, time_size, freq_size):

            pool_time = 3
            pool_freq = 3

            input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='Model_Input')

            conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same', name='conv1')(input_cnn)
            leaky = keras.layers.LeakyReLU(name='leaky1')(conv)

            conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same', name='conv2')(leaky)
            leaky = keras.layers.LeakyReLU(name='leaky2')(conv)

            max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3), name='max_pool1')(leaky)

            drop = keras.layers.Dropout(0.25, name='drop1')(max_pooling)
            # ------------------------------------------
            conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same', name='conv3')(drop)
            leaky = keras.layers.LeakyReLU(name='leaky3')(conv)

            conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same', name='conv4')(leaky)
            leaky = keras.layers.LeakyReLU(name='leaky4')(conv)

            max_pooling = keras.layers.MaxPooling2D(pool_size=(pool_time, pool_freq), name='max_pool2')(leaky)

            drop = keras.layers.Dropout(0.25, name='drop2')(max_pooling)
            # ------------------------------------------

            flat = keras.layers.Flatten(name='flat')(drop)

            # ------------------------------------------
            dense = keras.layers.Dense(512, name='dense1')(flat)
            leaky = keras.layers.LeakyReLU(name='leaky5')(dense)

            dense = keras.layers.Dense(256, name='dense2')(leaky)
            leaky = keras.layers.LeakyReLU(name='leaky6')(dense)

            out = keras.layers.Dense(1, activation='linear', name='dense_out')(leaky)

            sgd = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
            loss = keras.losses.mean_squared_error
            metric = keras.losses.mean_absolute_error

            model = keras.Model(inputs=input_cnn, outputs=out, name='encoder_1')
            model.compile(loss=loss, optimizer=sgd, metrics=[metric])

            model.load_weights(trained_encoder_path)
            return model

        def encoder_cnn(trained_cnn):
            for layer in trained_cnn.layers:
                if layer.name == "Model_Input":
                    sub_input_layer = layer
                if layer.name == "leaky6":
                    sub_output_layer = layer

            encoder = keras.Model(name='trained_submodel', inputs=sub_input_layer.input,
                                  outputs=sub_output_layer.output)
            return encoder

        trained_encoder_path = constants.trained_cnns_dir + '1/GNN_1_melspectrogram_6_3'
        trained_model = trained_cnn1(trained_encoder_path, 500, 256)
        encoder = encoder_cnn(trained_model)

        return encoder
