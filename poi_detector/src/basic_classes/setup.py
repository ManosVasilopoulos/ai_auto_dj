from .constants import project_dir
from .goodModels import GNN
import sys


class Setup:

    @staticmethod
    def __ask_new_setup():
        while 1:
            try:
                new_setup = input('New Model? (y/n) ')
                if new_setup == 'y' or new_setup == 'Y':
                    return True
                elif new_setup == 'n' or new_setup == 'n':
                    return False
                else:
                    print('Allowed choices "y", "Y", "n" or "N"')
            except KeyboardInterrupt:
                sys.exit()

    @staticmethod
    def __get_subsystem_type():
        while 1:
            try:
                subsystem_type = int(
                    input("Enter '1' for 'Relative Locator' or '2' for 'Preciser': "))
                if not 1 <= subsystem_type <= 2:
                    print("Wrong Subsystem Type. Please enter '1' or '2' only.")
                    continue
                break
            except KeyboardInterrupt:
                sys.exit()
            except ValueError:
                print("Wrong Subsystem Type. Please enter '1' or '2' only.")

        if subsystem_type == 1:
            return 'Relative Locator'
        elif subsystem_type == 2:
            return 'Preciser'
        else:
            raise Exception('Something went wrong. Finishing program...')

    @staticmethod
    def __check_subsystem_type(subsystem_type):
        if subsystem_type != 'Relative Locator' \
                and subsystem_type != 'Preciser':
            raise Exception('WrongSubSystemTypeError: Unknown subsystem type: "' + subsystem_type +
                            '" Please, enter one of the following-->'
                            '"Relative Locator", "Preciser"')

    @staticmethod
    def __get_id():
        while 1:
            try:
                _id = int(input('Good Model ID: '))
                break
            except ValueError:
                print('Choose a number starting from 1.')
            except KeyboardInterrupt:
                sys.exit()
        return _id

    @staticmethod
    def __get_transform_type():
        while 1:
            try:
                tt = input('Choose transform type: ')
                failed_condition = tt != 'spectrogram' and tt != 'melspectrogram' and tt != 'mfcc'
                if failed_condition:
                    print('Please choose one of the following transforms: (spectrogram, melspectrogram, mfcc) ')
                else:
                    break
            except KeyboardInterrupt:
                sys.exit()
        return tt

    @staticmethod
    def __get_batch_size():
        while 1:
            try:
                batch_size = int(input('Batch Size: '))
                if batch_size < 1:
                    print('• Choose a number bigger than 0 (zero).')
                else:
                    break
            except ValueError:
                print('• Choose a number bigger than 0 (zero).')
            except KeyboardInterrupt:
                sys.exit()
        return batch_size

    @staticmethod
    def __get_input_sizes(default=True):
        if default:
            return 500, 512
        else:
            while 1:
                try:
                    time_sz = int(input("Enter Time-Dimension's size: "))
                    condition = time_sz != 100 and time_sz != 250 and time_sz != 500 and time_sz != 750 and time_sz != 1000
                    if condition:
                        print('Please enter one of the accepted numbers: (100, 250, 500, 750, 1000)')
                    else:
                        break
                except ValueError:
                    print('Please enter one of the accepted numbers: (100, 250, 500, 750, 1000)')
                except KeyboardInterrupt:
                    sys.exit()
            while 1:
                try:
                    freq_sz = int(input("Enter Frequency-Dimension's size: "))
                    condition = freq_sz != 256 and freq_sz != 512 and freq_sz != 1024 and freq_sz != 2048
                    if condition:
                        print('Please enter one of the accepted numbers: (256, 512, 1024, 2048)')
                    else:
                        break
                except ValueError:
                    print('Please enter one of the accepted numbers: (256, 512, 1024, 2048)')
                except KeyboardInterrupt:
                    sys.exit()
            return time_sz, freq_sz

    @staticmethod
    def __ask_calculate_input():
        while 1:
            try:
                t = input('Calculate inputs? (y/n): ')
                if t == 'y' or t == 'Y' or t == 'yes' or t == 'Yes' or t == 'YES':
                    return True
                elif t == 'n' or t == 'N' or t == 'no' or t == 'No' or t == 'NO':
                    return False
                else:
                    print("Please enter 'yes' or 'no' only.")
            except KeyboardInterrupt:
                sys.exit()

    @staticmethod
    def __ask_unique_output():
        while 1:
            try:
                t = input('Unique output per input? (y/n) ')
                if t == 'y' or t == 'Y' or t == 'yes' or t == 'Yes' or t == 'YES':
                    return 'True'
                elif t == 'n' or t == 'N' or t == 'no' or t == 'No' or t == 'NO':
                    return 'False'
                else:
                    print("Please enter 'yes' or 'no' only.")
            except KeyboardInterrupt:
                sys.exit()

    """
        configs = {
                   'id': .. ,
                   'freq_size': .. ,
                   'time_size': .. ,
                   'batch_size': .. ,
                   'model_directory': .. ,
                   'subsystem_type': .. ,
                   'train_type': .. ,
                   'epochs': ..
                  }
    """

    def __init__(self, subsystem_type):
        self.__check_subsystem_type(subsystem_type)
        self.configs = {'epochs': 10, 'flag': True}
        self.logs = {'epoch': 0, 'point_song': '', 'model_to_load': 'NONE'}

        print("\n---------Welcome to Manos' Thesis---------")
        self.configs['subsystem_type'] = subsystem_type
        self.configs['id'] = self.__get_id()
        self.configs['transform_type'] = self.__get_transform_type()

        """ Ask if new setup """
        new_setup = self.__ask_new_setup()
        self.configs['calculate_input'] = new_setup
        """ Make the model's directory according to subsystem_type, id, transform_type """
        self.__make_model_directory_name()

        if new_setup:
            self.__select_configurations()
        else:
            self.__read_configurations()
            self.__read_log_file()

        in_size = (self.configs['time_size'], self.configs['freq_size'], 1)
        self.gnn = GNN(self.configs['subsystem_type'], self.configs['id'], in_size, self.configs['batch_size'])
        self.gnn.subsystem.model.summary()
        if not new_setup:
            self.gnn.subsystem.model.load_weights(self.configs['model_directory'] + self.logs['model_to_load'])

        self.logs['model_to_load'] = self.gnn.subsystem_name

        if new_setup:
            self.configs['calculate_input'] = self.__ask_calculate_input()
            self.configs['unique_output'] = self.__ask_unique_output()
            self.__save_to_configuration_file()

    """----------------------------------------------------------"""

    def __make_model_directory_name(self):
        self.configs['model_directory'] = project_dir + self.configs['subsystem_type'] + '/'
        self.configs['model_directory'] += str(self.configs['id']) + '/' + self.configs['transform_type'] + '/'

    """----------------------Configurations----------------------"""

    def __select_configurations(self):
        use_default = False
        if self.configs['subsystem_type'] == 'Relative Locator':
            self.configs['epochs'] = 10
        else:
            self.configs['epochs'] = 12
        self.configs['time_size'], self.configs['freq_size'] = self.__get_input_sizes(default=use_default)
        self.configs['batch_size'] = self.__get_batch_size()

    def __save_to_configuration_file(self):
        with open(self.configs['model_directory'] + 'config.txt', 'w+') as f:
            f.write('Neural Network Type: ' + str(self.configs['subsystem_type']) + '\n')
            f.write('Model ID: ' + str(self.configs['id']) + '\n')
            f.write('Transform Type: ' + self.configs['transform_type'] + '\n')
            f.write('Problem Type: ' + str(self.gnn.subsystem.problem_type) + '\n')
            f.write('Max Epochs: ' + str(self.configs['epochs']) + '\n')
            f.write('FFT-size of STFT: ' + str(self.configs['freq_size']) + '\n')
            f.write('Length of subspectrogram: ' + str(self.configs['time_size']) + '\n')
            f.write('Batch size: ' + str(self.configs['batch_size']) + '\n')
            f.write('Calculate input: ' + str(self.configs['calculate_input']) + '\n')
            f.write('Unique output per input: ' + str(self.configs['unique_output']) + '\n')

    def __read_configurations(self):
        with open(self.configs['model_directory'] + 'config.txt', 'r') as f:
            subsystem_type = f.readline().replace('Neural Network Type: ', '')
            self.configs['subsystem_type'] = subsystem_type.replace('\n', '')

            _id = f.readline().replace('Model ID: ', '')
            self.configs['id'] = int(_id.replace('\n', ''))

            transform_type = f.readline().replace('Transform Type: ', '')
            self.configs['transform_type'] = transform_type.replace('\n', '')

            problem_type = f.readline().replace('Problem Type: ', '')
            self.configs['problem_type'] = problem_type.replace('\n', '')

            epochs = f.readline().replace('Max Epochs: ', '')
            self.configs['epochs'] = int(epochs.replace('\n', ''))

            nfft = f.readline().replace('FFT-size of STFT: ', '')
            self.configs['freq_size'] = int(nfft.replace('\n', ''))

            time_size = f.readline().replace('Length of subspectrogram: ', '')
            self.configs['time_size'] = int(time_size.replace('\n', ''))

            batch_size = f.readline().replace('Batch size: ', '')
            self.configs['batch_size'] = int(batch_size)

            calculate_input = f.readline().replace('Calculate input: ', '')
            self.configs['calculate_input'] = calculate_input.replace('\n', '')

            unique_output = f.readline().replace('Unique output per input: ', '')
            temp = str(unique_output)
            if temp == 'True':
                self.configs['unique_output'] = True
            else:
                self.configs['unique_output'] = False

        self.configs['flag'] = False

    def __read_log_file(self):
        while 1:
            try:
                log_file_name = input('log_file: ')
                if not 'log_file_' in log_file_name:
                    print("Please Enter a log file's name with the following structure: 'log_file_day_month.txt'")
                else:
                    break
            except KeyboardInterrupt:
                sys.exit('Keyboard Interrupt.')
        with open(self.configs['model_directory'] + log_file_name, 'r') as f:
            epoch = f.readline().replace('Epoch: ', '')
            self.logs['epoch'] = int(epoch.replace('\n', ''))

            point_song = f.readline().replace('Last song used: ', '')
            self.logs['point_song'] = point_song.replace('\n', '')

            f.readline()
            model_to_load = f.readline().replace('Model: ', '')
            self.logs['model_to_load'] = model_to_load.replace('\n', '')
            return model_to_load

    def print_config(self):
        print('\n-----Configurations-----')
        print('Neural Network Type: ' + str(self.configs['subsystem_type']))
        print('Model ID: ' + str(self.configs['id']))
        print('Transform Type: ' + self.configs['transform_type'])
        print('Problem Type: ' + str(self.gnn.subsystem.problem_type))
        print('Max Epochs: ' + str(self.configs['epochs']) + '\n')
        print('FFT-size of STFT: ' + str(self.configs['freq_size']))
        print('Length of subspectrogram: ' + str(self.configs['time_size']))
        print('Batch size: ' + str(self.configs['batch_size']) + '\n')
        print('Calculate input: ' + str(self.configs['calculate_input']))
        print('Unique output per input: ' + str(self.configs['unique_output']))
