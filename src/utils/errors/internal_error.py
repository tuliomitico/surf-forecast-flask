class Error(Exception):
    """Base class for other exceptions"""
    pass

class InternalError(Error):
    def __init__(self, message: str , code: int = 500, description: str = None) -> None:
        self._code = code
        self._description = description
        self.message = message
        super().__init__(self, self.message)
        self.__name__ = self.__init__.__name__
