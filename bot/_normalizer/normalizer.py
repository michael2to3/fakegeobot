from abc import ABC, abstractmethod


class Normalizer(ABC):
    @staticmethod
    @abstractmethod
    def normalize(text: str) -> str:
        pass
