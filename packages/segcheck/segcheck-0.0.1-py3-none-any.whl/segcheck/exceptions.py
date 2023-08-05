"""segcheck uses a custom exception"""


class InvalidSegmentError(Exception):
    """This error is thrown when an invalid segment is found."""
    #def __init__(self, msg):
    #    super().__init__(msg)