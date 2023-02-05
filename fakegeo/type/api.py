class Api:
    _id: int
    _hash: str

    def __init__(self, api_id: int, api_hash):
        self._id = api_id
        self._hash = api_hash

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
