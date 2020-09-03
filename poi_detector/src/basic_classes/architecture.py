from abc import ABC, abstractmethod
from datetime import datetime
import pickle
import numpy as np
from os.path import join as os_path_join
from os import makedirs as os_makedirs


class Architecture(ABC):
    project_dir = 'D:/Documents/Thesis/Project Skaterbot/Good Neural Networks/'
    training_counter = 0
    training_samples = 0
    validation_counter = 0
    validation_samples = 0
    testing_counter = 0
    testing_samples = 0
    latest_epoch = 1
    max_epochs = 10

    arch_type: str

    def __init__(self, _id: int, batch_size: int, time_size: int, freq_size: int, transform_type: str,
                 window_size: float):
        self._id = _id
        self.batch_size = batch_size
        self.time_size = time_size
        self.freq_size = freq_size
        self.transform_type = transform_type
        self.window_size = window_size

    @abstractmethod
    def train(self, x: np.ndarray, y: np.ndarray, epoch: int):
        return

    @abstractmethod
    def train_with_validation(self, x: np.ndarray, y: np.ndarray, validation_data: tuple, epoch: int):
        return

    @abstractmethod
    def test(self, x: np.ndarray, y: np.ndarray, epoch: int):
        return

    @abstractmethod
    def predict(self, x: np.ndarray):
        return

    @abstractmethod
    def architecture(self, time_size: int, freq_size: int):
        return

    @abstractmethod
    def save_model(self):
        return

    @abstractmethod
    def load_trained_model(self):
        return

    def make_project_dir_url(self):
        new_project_dir = os_path_join(self.project_dir,
                                       self.arch_type,
                                       str(self._id),
                                       self.transform_type,
                                       str(self.window_size),
                                       str(self.time_size))
        return new_project_dir

    def make_project_dir(self):
        new_dir = self.make_project_dir_url()
        os_makedirs(new_dir, exist_ok=True)

        os_makedirs(os_path_join(new_dir, 'Train'), exist_ok=True)

        os_makedirs(os_path_join(new_dir, 'Test'), exist_ok=True)
        return new_dir

    def save_train_metrics(self, results: dict, epoch: int, model_name: str, counter_id: int):
        metrics = {}
        dir_extention = 'Train'
        for i, metric_name in enumerate(results):
            metrics[metric_name] = results[metric_name][0]

        metrics['model_name'] = model_name
        metrics['epoch'] = epoch
        metrics['id'] = counter_id
        metrics_path = os_path_join(self.project_dir, dir_extention, str(counter_id) + '_ep_' + str(epoch) + '.pkl')
        with open(metrics_path, 'wb') as pkl:
            pickle.dump(metrics, pkl, pickle.HIGHEST_PROTOCOL)

    def save_test_metrics(self, results: dict, epoch: int, model_name: str, counter_id: int, metrics_names: list):
        metrics = {}
        dir_extention = 'Test'
        for i, metric_name in enumerate(metrics_names):
            metrics[metric_name] = results[i]

        metrics['model_name'] = model_name
        metrics['epoch'] = epoch
        metrics['id'] = counter_id
        metrics_path = os_path_join(self.project_dir, dir_extention, str(counter_id) + '_ep_' + str(epoch) + '.pkl')
        with open(metrics_path, 'wb') as pkl:
            pickle.dump(metrics, pkl, pickle.HIGHEST_PROTOCOL)

    def save_log_file(self, model_name: str, epoch: int):
        dt = datetime.now()
        current_day = str(dt.day)
        current_month = str(dt.month)
        logs_path = os_path_join(self.project_dir, 'log_file_' + current_day + '_' + current_month + '.txt')
        with open(logs_path, 'w+') as f:
            f.write('Epoch: ' + str(epoch) + '\n')
            f.write('-------------------------\n')
            f.write('Model: ' + model_name + '\n')
            f.write('Training Samples: ' + str(self.training_samples) + '\n')
            f.write('Validation Samples: ' + str(self.validation_samples) + '\n')
            f.write('Testing Samples: ' + str(self.testing_samples) + '\n')

    def load_log_file(self):
        import sys
        while 1:
            try:
                log_file_name = input('log_file: ')
                if 'log_file_' not in log_file_name:
                    print("Please Enter a log file's name with the following structure: 'log_file_day_month.txt'")
                else:
                    break
            except KeyboardInterrupt:
                sys.exit('Keyboard Interrupt.')

        logs_path = os_path_join(self.project_dir, log_file_name + '.txt')
        with open(logs_path, 'w+') as f:
            epoch = f.readline().replace('Epoch: ', '')
            self.latest_epoch = int(epoch.replace('\n', ''))

    def reset_counters(self):
        self.training_counter = 0
        self.training_samples = 0
        self.validation_counter = 0
        self.validation_samples = 0
        self.testing_counter = 0
        self.testing_samples = 0

    def save_checkpoint(self, song_id: int, epoch: int, training_mode: bool):
        import pandas as pd

        checkpoint = pd.DataFrame({'last_song_id': song_id,
                                   'last_epoch': epoch,
                                   'training': training_mode,
                                   'testing': not training_mode,
                                   'training_counter': self.training_counter,
                                   'training_samples': self.training_samples,
                                   'validation_counter': self.validation_counter,
                                   'validation_samples': self.validation_samples,
                                   'testing_counter': self.testing_counter,
                                   'testing_samples': self.testing_samples}, index=[0])
        check_point_path = os_path_join(self.project_dir, 'train_test_checkpoint.csv')
        checkpoint.to_csv(check_point_path)

    def load_checkpoint(self):
        import pandas as pd

        dataframe_path = os_path_join(self.project_dir, 'train_test_checkpoint.csv')
        dataframe = pd.read_csv(dataframe_path)
        temp_checkpoint = dataframe.to_dict()

        checkpoint = {'last_song_id': temp_checkpoint['last_song_id'][0],
                      'last_epoch': temp_checkpoint['last_epoch'][0],
                      'training': temp_checkpoint['training'][0],
                      'testing': temp_checkpoint['testing'][0],
                      'training_counter': temp_checkpoint['training_counter'][0],
                      'training_samples': temp_checkpoint['training_samples'][0],
                      'validation_counter': temp_checkpoint['validation_counter'][0],
                      'validation_samples': temp_checkpoint['validation_samples'][0],
                      'testing_counter': temp_checkpoint['testing_counter'][0],
                      'testing_samples': temp_checkpoint['testing_samples'][0]
                      }
        self.latest_epoch = temp_checkpoint['last_epoch'][0]
        self.training_counter = temp_checkpoint['training_counter'][0]
        self.training_samples = temp_checkpoint['training_samples'][0]
        self.validation_counter = temp_checkpoint['validation_counter'][0]
        self.validation_counter = temp_checkpoint['validation_samples'][0]
        self.testing_counter = temp_checkpoint['testing_counter'][0]
        self.testing_samples = temp_checkpoint['testing_samples'][0]
        return checkpoint
