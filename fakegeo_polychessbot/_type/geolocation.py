from telethon.types import InputMediaGeoLive, InputGeoPoint
import json


class Geolocation:
    _lat: float
    _long: float
    _timeout: int

    def __init__(self, lat: float, long: float, timeout: int):
        self._lat = lat
        self._long = long
        self._timeout = timeout

    def get_input_media_geo_live(self):
        return InputMediaGeoLive(
            InputGeoPoint(self._lat, self._long), period=self._timeout
        )

    def to_json(self) -> str:
        data = {
            "lat": self._lat,
            "long": self._long,
            "timeout": self._timeout,
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "Geolocation":
        data = json.loads(json_str)
        return cls(data["lat"], data["long"], data["timeout"])

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value):
        self._long = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value
