from telethon.types import InputMediaGeoLive, InputGeoPoint
import json


class Geolocation:
    _lat: float
    _long: float
    _interval: int

    def __init__(self, lat: float, long: float, interval: int):
        self._lat = lat
        self._long = long
        self._interval = interval

    def get_input_media_geo_live(self):
        return InputMediaGeoLive(
            InputGeoPoint(self._lat, self._long), period=self._interval
        )

    def to_json(self) -> str:
        data = {
            "lat": self._lat,
            "long": self._long,
            "interval": self._interval,
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "Geolocation":
        data = json.loads(json_str)
        return cls(data["lat"], data["long"], data["interval"])

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
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    def __str__(self):
        return f"Geolocation(lat={self._lat}, long={self._long}, interval={self._interval})"
