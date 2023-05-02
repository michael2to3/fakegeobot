class ApiApp:
    __slots__ = ("_id", "_hash")

    def __init__(self, api_id: int, api_hash):
        self._id = api_id
        self._hash = api_hash

    def __eq__(self, other):
        return self._id == other._id and self._hash == other._hash

    @property
    def id(self):
        return self._id

    @property
    def hash(self):
        return self._hash
