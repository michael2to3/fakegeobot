class Api:
    _api_id: int
    _api_hash: str

    def __init__(self, api_id: int, api_hash):
        self._api_id = api_id
        self._api_hash = api_hash

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
