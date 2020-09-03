from abc import ABC, abstractmethod


class NN(ABC):

    def __init__(self, _id: int):
        self._id = _id

    @abstractmethod
    def get_model(self, time_size: int, freq_size: int):
        return
