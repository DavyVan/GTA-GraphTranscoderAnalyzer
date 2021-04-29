import abc
from scipy.sparse import csr_matrix


class OutputBase(metaclass=abc.ABCMeta):
    """
    This is the base class of graph writer for all supported output format.
    User can implement this abstract class to support new format.

    """
    @abc.abstractmethod
    def to_target_format(self, _IR: csr_matrix):
        """
        This abstract method must be implemented for all input format, converting the graph from ``IR`` to the target output format.
        This function should be called inside :func:`write_to_file()`.

        :param _IR: The graph in ``IR``.
        :return: The graph in target format.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def write_to_file(self, _IR: csr_matrix) -> None:
        """
        No need to convert from IR to target format, which is handled by another method :func:`to_target_format()`.
        This function should call :func:`to_target_format()`.

        :param _IR: The graph in ``IR``.
        :return: None
        """
        raise NotImplementedError
