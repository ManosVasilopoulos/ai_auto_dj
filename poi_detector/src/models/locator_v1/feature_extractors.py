from tensorflow import keras
from joblib import load as pca_load
from os.path import join as pathjoin
from sklearn.decomposition import IncrementalPCA
from abc import ABC, abstractmethod, ABCMeta
import numpy as np


class FeatureExtractor(ABC, metaclass=ABCMeta):

    @abstractmethod
    def extract_features(self, x):
        pass

    def extract_batch_features(self, x_batch):
        x_feats_batch = []
        for x in x_batch:
            x_feats = self.extract_features(x)
            x_feats_batch.append(x_feats)
        return np.array(x_feats_batch)


class FeatureExtractorCNN(FeatureExtractor):
    cnn_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\Good Neural Networks\\Preciser v1'

    cnn_feat_extractor: keras.Model

    def load_feature_extractor(self, _id: int, transform_type: str, window_size: float, time_size: int, freq_size: int,
                               last_layer_name: str):
        architecture = self.__get_arch(_id, time_size, freq_size)

        trained_model_path = self.get_project_dir(_id, transform_type, window_size, time_size)
        architecture.load_weights(trained_model_path)

        last_layer = self.__get_last_layer(architecture, last_layer_name)

        self.cnn_feat_extractor = keras.Model(inputs=architecture.inputs, outputs=last_layer)
        return self.cnn_feat_extractor, self.cnn_feat_extractor.output_shape[1]

    def __get_last_layer(self, trained_model: keras.Model, last_layer_name: str):
        last_layer = None
        for layer in trained_model.layers:
            if layer.name == last_layer_name:
                last_layer = layer
                break
        if not last_layer:
            raise Exception('FeatureExtractorError: The layer "' + last_layer_name + '" does not exist.')
        return last_layer

    def __get_arch(self, _id: int, time_size: int, freq_size: int):
        if _id == 7:
            cnn_arch = self.__cnn7(time_size, freq_size)
        elif _id == 8:
            cnn_arch = self.__cnn8(time_size, freq_size)
        else:
            raise Exception(
                'FeatureExtractorError: rnn with id higher or equal to "' + str(_id) + '" does not exist.')
        return cnn_arch

    def get_project_dir(self, _id: int, transform_type: str, window_size: float, time_size: int):
        new_project_dir = pathjoin(self.cnn_dir,
                                   str(_id),
                                   transform_type,
                                   str(window_size),
                                   str(time_size))
        return new_project_dir

    """ FOR SPECTROGRAMS AND MELSPECTROGRAMS """

    def __cnn7(self, time_size: int, freq_size: int):
        from tensorflow.keras.regularizers import l2

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

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3), name='final_max_pool')(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024, kernel_regularizer=l2(0.001), name='dense_features_1')(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-7_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-7')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        return model

    """ FOR Constant-Q ONLY """

    def __cnn8(self, time_size: int, freq_size: int):
        from tensorflow.keras.regularizers import l2

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

        conv = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding='same')(leaky)
        leaky = keras.layers.LeakyReLU()(conv)

        max_pooling = keras.layers.MaxPooling2D(pool_size=(3, 3), name='final_max_pool')(leaky)

        drop = keras.layers.Dropout(0.25)(max_pooling)
        # ------------------------------------------

        flat = keras.layers.Flatten(name='flat')(drop)

        # ------------------------------------------
        dense = keras.layers.Dense(1024, kernel_regularizer=l2(0.001), name='dense_features_1')(flat)
        leaky = keras.layers.LeakyReLU()(dense)

        out = keras.layers.Dense(1, activation='linear', name='preciser-8_output')(leaky)

        optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        loss = keras.losses.mean_squared_error
        metric1 = keras.losses.mean_squared_error
        metric0 = keras.losses.mean_absolute_error

        model = keras.Model(inputs=input_cnn, outputs=out, name='Preciser_v1-7')
        model.compile(loss=loss, optimizer=optimizer, metrics=[metric0, metric1])

        return model

    def extract_features(self, x_batch):
        Y = self.cnn_feat_extractor.predict(x=x_batch)
        return Y


class FeatureExtractorPCA(FeatureExtractor):
    pca_dir = 'D:\\Documents\\Thesis\\Project Skaterbot\\PCA'

    i_pca: IncrementalPCA

    def load_feature_extractor(self, transform_type: str, window_size: float, time_size: int, freq_size: int):
        pca_dir = self.get_project_dir(transform_type, window_size, time_size, freq_size)
        pca_path = pathjoin(pca_dir, 'pca_' + transform_type + '.joblib')
        self.i_pca = pca_load(pca_path)
        return self.i_pca, self.i_pca.n_components

    def extract_features(self, x_batch):
        x_batch = self.__transform_ims_to_vecs(x_batch)
        Y = self.i_pca.transform(X=x_batch)
        return Y

    def get_project_dir(self, transform_type: str, window_size: float, time_size: int, freq_size: int):
        new_project_dir = pathjoin(self.pca_dir,
                                   transform_type,
                                   str(window_size),
                                   str(time_size),
                                   str(freq_size))
        return new_project_dir

    # One sample
    @staticmethod
    def __transform_ims_to_vecs(x_train):
        time_steps = x_train.shape[0]
        dim_1 = x_train.shape[1]
        dim_2 = x_train.shape[2]
        vec_length = dim_1 * dim_2

        time_steps_x = []
        for j in range(time_steps):
            time_step = np.reshape(x_train[j], vec_length)
            time_steps_x.append(time_step)
        time_steps_x = np.array(time_steps_x)

        return time_steps_x

