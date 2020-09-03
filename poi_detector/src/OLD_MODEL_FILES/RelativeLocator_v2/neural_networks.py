from basic_classes.neural_networks import NN
from tensorflow import keras


class CNN(NN):
    model_version = 'Relative-Locator_v2'

    def get_model(self, time_size: int, freq_size: int):
        if self._id == 1:
            cnn_model, metrics_name = self.__cnn1(time_size, freq_size)
        else:
            raise Exception('CNN: cnn with id higher or equal to "', self._id, '" does not exist.')

        return cnn_model, metrics_name

    def __cnn1(self, time_size, freq_size):
        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name=self.model_version + '_input')

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU(name='leaky3')(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        dense = keras.layers.Dense(512)(leaky)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name=self.model_version + '_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric0 = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.metrics.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name=self.model_version + '-1')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1, metric2])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names
