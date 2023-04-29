from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    async def execute(self) -> None:
        pass
