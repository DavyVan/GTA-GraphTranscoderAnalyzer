import abc


class InputBase(metaclass=abc.ABCMeta):
    """
    This is the base class of graph reader for all supported input format.
    User can implement this abstract class to support new format.

    """

    @abc.abstractmethod
    def read_from_file(self) -> None:
        """
        This abstract method must be implemented for all input format, reading the graph from file into memory.
        No need to convert to the intermediate format, which is handled by another method :func:`to_ir()`.

        :return: None. The graph will be stored internally.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_ir(self):
        """
        This abstract method must be implemented for all input format, converting the graph from input format to the intermediate format.

        :return: The graph in the IR.
        """
        raise NotImplementedError
