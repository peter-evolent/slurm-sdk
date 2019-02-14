"""Custom exception classes for Slurm SDK"""


class SDKException(Exception):
    """The base exception class for all exceptions this library raises."""
    def __init__(self, message=None, data=None):
        self.message = self.__class__.__name__ if message is None else message
        self.data = data if data else {}
        super(SDKException, self).__init__(self.message)
