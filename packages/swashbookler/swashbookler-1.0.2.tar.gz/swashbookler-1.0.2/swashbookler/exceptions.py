import requests


class NetworkError(requests.RequestException):
    pass


class ParsingError(RuntimeError):
    pass
