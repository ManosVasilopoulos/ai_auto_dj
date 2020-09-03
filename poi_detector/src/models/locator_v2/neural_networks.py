from poi_detector.src.basic_classes.neural_networks import NN
from tensorflow import keras


class CNN(NN):

    def __init__(self, _id):
        super().__init__(_id)

    def get_model(self, time_size, freq_size):
        if self._id == 1:
            return self.__cnn1(time_size, freq_size)
        elif self._id == 2:
            return self.__cnn2(time_size, freq_size)
        elif self._id == 3:
            return self.__cnn3(time_size, freq_size)
        elif self._id == 4:
            return self.__cnn4(time_size, freq_size)
        elif self._id == 5:
            return self.__cnn5(time_size, freq_size)
        elif self._id == 6:
            return self.__cnn6(time_size, freq_size)
        elif self._id == 7:
            return self.__cnn7(time_size, freq_size)
        else:
            raise Exception(
                'CNN: cnn with id higher or equal to "' + str(self._id) + '" does not exist.')

    def __cnn1(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

        conv = keras.layers.Conv2D(filters=8, kernel_size=(5, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=8, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=32, kernel_size=(5, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(5, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(5, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=128, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-1_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Locator_v2-1')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    # RESNET
    def __cnn2(self, time_size, freq_size):
        from tensorflow.keras.applications import ResNet50

        input_shape = (time_size, freq_size, 1)
        resnet = ResNet50(include_top=False, weights=None, input_tensor=None, input_shape=input_shape, pooling='avg')

        dense = keras.layers.Dense(1024, name='dense1', activation='relu')(resnet.outputs[0])

        dense = keras.layers.Dense(512, name='dense2', activation='relu')(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-2_output')(dense)

        optimizer = keras.optimizers.SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=resnet.inputs[0], outputs=out, name='Locator_v2-2')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    def __cnn3(self, time_size, freq_size):
        from tensorflow.keras.applications.inception_v3 import InceptionV3

        inception = InceptionV3(include_top=False,
                                weights=None,
                                pooling='max',
                                input_shape=(time_size, freq_size, 1))
        dense = keras.layers.Dense(1024, name='dense1', activation='relu')(inception.outputs[0])

        dense = keras.layers.Dense(512, name='dense2', activation='relu')(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-3_output')(dense)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=inception.inputs[0], outputs=out, name='Locator_v2-3')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    def __cnn4(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

        conv = keras.layers.Conv2D(filters=8, kernel_size=(3, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=8, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-1_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Locator_v2-4')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    def __cnn5(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(512)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-5_output')(leaky)

        # optimizer = keras.optimizers.SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)
        optimizer = keras.optimizers.Adam(lr=0.00001)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Locator_v2-5')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    def __cnn6(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(128)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-6_output')(leaky)

        # optimizer = keras.optimizers.SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)
        optimizer = keras.optimizers.Adam(lr=0.0001)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Locator_v2-6')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names

    def __cnn7(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

        filters = 32

        conv = keras.layers.Conv2D(filters=filters, kernel_size=(3, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=filters, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)

        filters *= 2
        for i in range(1, 3):
            conv = keras.layers.Conv2D(filters=filters, kernel_size=(3, 3), padding='same')(drop)
            leaky = keras.layers.LeakyReLU()(conv)

            conv = keras.layers.Conv2D(filters=filters, kernel_size=(3, 3), padding='same')(leaky)
            leaky = keras.layers.LeakyReLU()(conv)

            max_pooling = keras.layers.MaxPooling2D(pool_size=(2, 2))(leaky)

            drop = keras.layers.Dropout(0.25)(max_pooling)

            filters *= 2

        conv = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.GlobalMaxPooling2D()(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(128)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(time_size, activation='sigmoid', name='locator-7_output')(leaky)

        # optimizer = keras.optimizers.SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)
        optimizer = keras.optimizers.Adam(lr=0.0001)
        loss = keras.losses.binary_crossentropy
        metric1 = keras.metrics.binary_accuracy
        metric2 = keras.losses.mean_absolute_error
        metric3 = keras.losses.mean_squared_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Locator_v2-5')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric1, metric2, metric3])

        metrics_names = ['loss', metric1.__name__, metric2.__name__, metric3.__name__]

        return model, metrics_names
