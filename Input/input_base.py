import abc

class InputBase(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def read_from_file(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def to_IR(self):
        raise NotImplementedError