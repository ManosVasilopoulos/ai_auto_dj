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
        elif self._id == 8:
            return self.__cnn8(time_size, freq_size)
        elif self._id == 9:
            return self.__cnn9(time_size, freq_size)
        else:
            raise Exception(
                'CNN: cnn with id higher or equal to "' + str(self._id) + '" does not exist.')

    def __cnn1(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

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
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(512)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-1_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-1')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names

    # RESNET
    def __cnn2(self, time_size, freq_size):
        from tensorflow.keras.applications import ResNet50

        input_shape = (time_size, freq_size, 1)
        resnet = ResNet50(include_top=False, weights=None, input_tensor=None, input_shape=input_shape, pooling='avg')

        dense = keras.layers.Dense(256, activation='relu')(resnet.outputs[0])

        dense = keras.layers.Dense(1, name='dense_out')(dense)

        new_model = keras.Model(inputs=resnet.inputs[0], outputs=dense, name='Preciser_v1-2')

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        # optimizer = keras.optimizers.Adam()
        loss = keras.losses.mean_squared_error
        metric0 = keras.metrics.mean_squared_error
        metric1 = keras.metrics.mean_absolute_error

        new_model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return new_model, metrics_names

    def __cnn3(self, time_size, freq_size):
        from tensorflow.keras.applications.inception_v3 import InceptionV3

        inception = InceptionV3(include_top=False,
                                weights=None,
                                pooling='avg',
                                input_shape=(time_size, freq_size, 1))
        dense = keras.layers.Dense(1024, name='dense1', activation='relu')(inception.outputs[0])

        dense = keras.layers.Dense(512, name='dense2', activation='relu')(dense)

        dense = keras.layers.Dense(1, name='dense_out')(dense)

        new_model = keras.Model(inputs=inception.inputs[0], outputs=dense, name='Preciser_v1-3')

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        # optimizer = keras.optimizers.Adam()
        loss = keras.losses.mean_squared_error
        metric0 = keras.metrics.mean_squared_error
        metric1 = keras.metrics.mean_absolute_error

        new_model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return new_model, metrics_names

    def __cnn4(self, time_size, freq_size):
        # create model
        def inception(x, filters):
            # 1x1
            path1 = keras.layers.Conv2D(filters=filters[0], kernel_size=(1, 1), strides=1, padding='same',
                                        activation='relu')(x)

            # 1x1->3x3
            path2 = keras.layers.Conv2D(filters=filters[1][0], kernel_size=(1, 1), strides=1, padding='same',
                                        activation='relu')(x)
            path2 = keras.layers.Conv2D(filters=filters[1][1], kernel_size=(3, 3), strides=1, padding='same',
                                        activation='relu')(
                path2)

            # 1x1->5x5
            path3 = keras.layers.Conv2D(filters=filters[2][0], kernel_size=(1, 1), strides=1, padding='same',
                                        activation='relu')(x)
            path3 = keras.layers.Conv2D(filters=filters[2][1], kernel_size=(5, 5), strides=1, padding='same',
                                        activation='relu')(
                path3)

            # 3x3->1x1
            path4 = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=1, padding='same')(x)
            path4 = keras.layers.Conv2D(filters=filters[3], kernel_size=(1, 1), strides=1, padding='same',
                                        activation='relu')(path4)

            return keras.layers.Concatenate(axis=-1)([path1, path2, path3, path4])

        def auxiliary(x, name=None):
            layer = keras.layers.AveragePooling2D(pool_size=(5, 5), strides=3, padding='valid')(x)
            layer = keras.layers.Conv2D(filters=128, kernel_size=(1, 1), strides=1, padding='same', activation='relu')(
                layer)
            layer = keras.layers.Flatten()(layer)
            layer = keras.layers.Dense(units=256, activation='relu')(layer)
            layer = keras.layers.Dropout(0.4)(layer)
            layer = keras.layers.Dense(units=1, activation='linear', name=name)(layer)
            return layer

        def googlenet():
            layer_in = keras.layers.Input(shape=(time_size, freq_size, 1))

            # stage-1
            layer = keras.layers.Conv2D(filters=64, kernel_size=(7, 7), strides=2, padding='same', activation='relu')(
                layer_in)
            layer = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(layer)
            layer = keras.layers.BatchNormalization()(layer)

            # stage-2
            layer = keras.layers.Conv2D(filters=64, kernel_size=(1, 1), strides=1, padding='same', activation='relu')(
                layer)
            layer = keras.layers.Conv2D(filters=192, kernel_size=(3, 3), strides=1, padding='same', activation='relu')(
                layer)
            layer = keras.layers.BatchNormalization()(layer)
            layer = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(layer)

            # stage-3
            layer = inception(layer, [64, (96, 128), (16, 32), 32])  # 3a
            layer = inception(layer, [128, (128, 192), (32, 96), 64])  # 3b
            layer = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(layer)

            # stage-4
            layer = inception(layer, [192, (96, 208), (16, 48), 64])  # 4a
            aux1 = auxiliary(layer, name='aux1')
            layer = inception(layer, [160, (112, 224), (24, 64), 64])  # 4b
            layer = inception(layer, [128, (128, 256), (24, 64), 64])  # 4c
            layer = inception(layer, [112, (144, 288), (32, 64), 64])  # 4d
            aux2 = auxiliary(layer, name='aux2')
            layer = inception(layer, [256, (160, 320), (32, 128), 128])  # 4e
            layer = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(layer)

            # stage-5
            layer = inception(layer, [256, (160, 320), (32, 128), 128])  # 5a
            layer = inception(layer, [384, (192, 384), (48, 128), 128])  # 5b
            layer = keras.layers.AveragePooling2D(pool_size=(7, 7), strides=1, padding='valid')(layer)

            # stage-6
            layer = keras.layers.Flatten()(layer)
            layer = keras.layers.Dropout(0.4)(layer)
            layer = keras.layers.Dense(units=256, activation='linear')(layer)
            main = keras.layers.Dense(units=1, activation='linear', name='main')(layer)

            model = keras.models.Model(inputs=layer_in, outputs=[main, aux1, aux2])

            return model

        google_net = googlenet()

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        # optimizer = keras.optimizers.Adam()
        loss = keras.losses.mean_squared_error
        metric0 = keras.metrics.mean_squared_error
        metric1 = keras.metrics.mean_absolute_error

        google_net.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return google_net, metrics_names

    # Same as __cnn1 but with one extra dense layer
    def __cnn5(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

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
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(512)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        dense = keras.layers.Dense(128)(leaky)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-5_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-5')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names

        # Same as __cnn1 but with one extra dense layer

    def __cnn6(self, time_size, freq_size):

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-1_input')

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
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024)(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-6_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-6')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names

    def __cnn7(self, time_size, freq_size):
        from tensorflow.keras.regularizers import l2

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-7_input')

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
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024, kernel_regularizer=l2(0.001))(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-7_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-8')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names

    """ FOR Constant-Q ONLY """
    def __cnn8(self, time_size, freq_size):
        from tensorflow.keras.regularizers import l2

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-8_input')

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
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024, kernel_regularizer=l2(0.001))(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-8_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-8')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names

    """ FOR MFCC ONLY """
    def __cnn9(self, time_size, freq_size):
        from tensorflow.keras.regularizers import l2

        input_cnn = keras.layers.Input(shape=(time_size, freq_size, 1), name='preciser-9_input')

        conv = keras.layers.Conv2D(filters=32, kernel_size=(5, 3), padding='same')(input_cnn)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=16, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=64, kernel_size=(5, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=32, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------
        conv = keras.layers.Conv2D(filters=128, kernel_size=(5, 3), padding='same')(drop)
        leaky = keras.layers.LeakyReLU()(conv)

        conv = keras.layers.Conv2D(filters=64, kernel_size=(5, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(4, 2))(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024, kernel_regularizer=l2(0.001))(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-9_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-9')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        metrics_names = ['loss', metric0.__name__, metric1.__name__]

        return model, metrics_names