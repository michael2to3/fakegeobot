import logging
from typing import Callable, List, Any, Coroutine
import asyncio
import schedule
from croniter import croniter
import time


class FloodException(BaseException):
    __slots__ = ("message",)

    def __init__(self, message: str):
        self.message = message


class Cron:
    __slots__ = ("_logger", "_callback", "_expression", "_timeout", "_job")

    _logger: logging.Logger
    _callback: Callable[[], Coroutine[Any, Any, None]]
    _expression: str
    _timeout: int
    _job: Any

    def __init__(
        self,
        callback: Callable[[], Coroutine[Any, Any, None]],
        expression: str,
        timeout: int,
    ):
        self._logger = logging.getLogger(__name__)
        self._callback = callback
        self._expression = expression
        self._timeout = timeout
        self.validate_expression()
        self._job = None

    def validate_expression(self):
        cron_parts = self._expression.split()
        if len(cron_parts) < 5:
            raise ValueError("Invalid cron expression")

        mins: str = cron_parts[0]
        if mins == "*":
            raise FloodException("Cron schedule is too frequent")

        if "-" in mins or "," in mins or "/" in mins:
            min_values: List[int] = []
            if "-" in mins:
                min_range: List[int] = list(map(int, mins.split("-")))
                min_values = list(range(min_range[0], min_range[1] + 1))
            elif "," in mins:
                min_values = list(map(int, mins.split(",")))
            elif "/" in mins:
                min_step: int = int(mins.split("/")[1])
                min_values = list(range(0, 60, min_step))

            if any(
                t2 - t1 < self._timeout / 60
                for t1, t2 in zip(min_values, min_values[1:])
            ):
                raise FloodException("Cron schedule is too frequent")

    async def start(self):
        self._logger.info("Starting cron")
        if self._job is None:
            self._job = asyncio.ensure_future(self._schedule_runner())

    async def _schedule_runner(self):
        iter = croniter(self._expression, time.time())
        while True:
            next_run = iter.get_next(float)
            await asyncio.sleep(next_run - time.time())
            await self._async_callback_wrapper()

    async def _async_callback_wrapper(self):
        self._logger.info("Start callback in cron")
        await self._callback()

    async def stop(self):
        self._logger.info("Stopping cron")
        if self._job:
            self._job.cancel()
            self._job = None

    def __str__(self) -> str:
        return self._expression

    @property
    def expression(self) -> str:
        return self._expression

    @property
    def timeout(self) -> int:
        return self._timeout
