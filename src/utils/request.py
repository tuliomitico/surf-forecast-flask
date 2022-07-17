import requests

class Request():
    def __init__(self, request = requests):
        self.__request = request

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.__request.get(url,**kwargs)

    @staticmethod
    def is_request_error(error: requests.ConnectionError) -> bool:
        return bool(error.response and error.response.status)
