import abc

class OutputBase(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def to_target_format(self, _IR):
        raise NotImplementedError

    @abc.abstractclassmethod
    def write_to_file(self, _IR):
        raise NotImplementedError