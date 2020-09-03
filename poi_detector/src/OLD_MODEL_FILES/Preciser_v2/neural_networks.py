from basic_classes.neural_networks import NN
from tensorflow import keras


class CNN(NN):

    def __init__(self, _id):
        super().__init__(_id)

    def get_model(self, time_size, freq_size):
        if self._id == 1:
            return self.__cnn1(time_size, freq_size)
        if self._id == 2:
            return self.__cnn2(time_size, freq_size)
        else:
            raise Exception(
                'CNN: cnn with id higher or equal to "' + str(self._id) + '" does not exist.')

    def __cnn1(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='Model_Input')

        conv = keras.layers.Conv2D(filters=32,
                                   kernel_size=(3, 3),
                                   padding='same',
                                   name='conv1')(input_cnn)
        leaky = keras.layers.LeakyReLU(name='leaky1')(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same',
                                   name='conv2')(leaky)
        leaky = keras.layers.LeakyReLU(name='leaky2')(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3), name='max_pool1')(leaky)

        drop = keras.layers.Dropout(0.2)(max_pooling)

        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same',
                                   name='conv3')(drop)
        leaky = keras.layers.LeakyReLU(name='leaky3')(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same',
                                   name='conv4')(leaky)
        leaky = keras.layers.LeakyReLU(name='leaky4')(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3), name='max_pool2')(leaky)

        drop = keras.layers.Dropout(0.2)(max_pooling)

        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024, name='dense1')(flat)
        leaky = keras.layers.LeakyReLU(name='leaky9')(dense)

        dense = keras.layers.Dense(512, name='dense2')(leaky)
        leaky = keras.layers.LeakyReLU(name='leaky10')(dense)

        dense = keras.layers.Dense(256, name='dense3')(leaky)
        leaky = keras.layers.LeakyReLU(name='leaky11')(dense)

        out = keras.layers.Dense(time_size, activation='softmax', name='dense_out')(leaky)

        #optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        optimizer = keras.optimizers.Adam()
        loss = keras.losses.sparse_categorical_crossentropy
        metric0 = keras.metrics.sparse_categorical_crossentropy
        metric1 = keras.metrics.categorical_accuracy
        metric2 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v2-1')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1, metric2])

        metrics_names = ['loss', metric0.__name__, metric1.__name__, metric2.__name__]

        return model, metrics_names

    # RESNET
    def __cnn2(self, time_size, freq_size):
        from tensorflow.keras.applications import ResNet50

        input_shape = (time_size, freq_size, 1)
        model = ResNet50(include_top=False, weights=None, input_tensor=None, input_shape=input_shape, pooling='avg')

        dense = keras.layers.Dense(1024, name='dense1', activation='relu')(model.outputs[0])

        dense = keras.layers.Dense(512, name='dense2', activation='relu')(dense)

        dense = keras.layers.Dense(time_size, activation='softmax', name='dense_out')(dense)

        new_model = keras.Model(inputs=model.inputs[0], outputs=dense, name='Preciser_v2-2')

        sgd = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.sparse_categorical_crossentropy
        metric0 = keras.metrics.sparse_categorical_crossentropy
        metric1 = keras.metrics.categorical_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        new_model.compile(loss=loss, optimizer=sgd, metrics=[metric0, metric1, metric2, metric3])

        metrics_names = ['loss', metric0.__name__, metric1.__name__, metric2.__name__, metric3.__name__]

        return new_model, metrics_names

    def __cnn3(self, time_size, freq_size):
        from tensorflow.keras.applications.inception_v3 import InceptionV3

        inception = InceptionV3(include_top=False,
                                weights=None,
                                pooling='max',
                                input_shape=(time_size, freq_size, 1))
        dense = keras.layers.Dense(1024, name='dense1', activation='relu')(inception.outputs[0])

        dense = keras.layers.Dense(512, name='dense2', activation='relu')(dense)

        dense = keras.layers.Dense(time_size, activation='softmax', name='dense_out')(dense)

        new_model = keras.Model(inputs=inception.inputs[0], outputs=dense, name='Preciser_v2-3')

        sgd = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.sparse_categorical_crossentropy
        metric0 = keras.metrics.sparse_categorical_crossentropy
        metric1 = keras.metrics.categorical_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        new_model.compile(loss=loss, optimizer=sgd, metrics=[metric0, metric1, metric2, metric3])

        metrics_names = ['loss', metric0.__name__, metric1.__name__, metric2.__name__, metric3.__name__]

        return new_model, metrics_names
