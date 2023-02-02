from telethon.types import InputMediaGeoLive, InputGeoPoint


class Geolocation:
    _lat: float
    _long: float
    _timeout: int

    def __init__(self):
        self._lat = 59.965128
        self._long = 30.398474
        self._timeout = 60

    def set_location(self, lat: float, long: float) -> None:
        self._lat = lat
        self._long = long

    def set_timeout(self, timeout: int) -> None:
        self._timeout = timeout

    def get(self):
        return InputMediaGeoLive(
            InputGeoPoint(self._lat, self._long),
            period=self._timeout
        )
