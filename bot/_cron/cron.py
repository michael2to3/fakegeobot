import asyncio
import logging
import time
from typing import Any, Callable, Coroutine
from croniter import croniter
from .._config import Config


class FloodException(BaseException):
    __slots__ = ("message",)

    def __init__(self, message: str):
        self.message = message


class Cron:
    __slots__ = (
        "_logger",
        "_callback",
        "_expression",
        "_timeout",
        "_job",
        "_last_callback_time",
    )

    _logger: logging.Logger
    _callback: Callable[[], Coroutine[Any, Any, None]]
    _expression: str
    _timeout: int
    _job: Any
    _last_callback_time: float

    def __init__(
        self,
        callback: Callable[[], Coroutine[Any, Any, None]],
        expression: str,
        timeout: int | None = None,
    ):
        self._logger = logging.getLogger(__name__)
        self._callback = callback
        self._expression = expression
        self._timeout = timeout if timeout is not None else Config().cron_timeout
        self._job = None
        self._last_callback_time = 0

    def start(self):
        self._logger.info("Starting cron")
        if self._job is None:
            self._job = asyncio.ensure_future(self._schedule_runner())

    def is_running(self) -> bool:
        return self._job is not None

    async def _schedule_runner(self):
        iter = croniter(self._expression, time.time())
        while True:
            next_run = iter.get_next(float)
            await asyncio.sleep(next_run - time.time())
            current_time = time.time()
            if current_time - self._last_callback_time >= self._timeout:
                self._logger.info("Scheduling callback")
                await self._async_callback_wrapper()
                self._last_callback_time = current_time
            else:
                self._logger.info(
                    f"Sleeping {self._timeout - (current_time - self._last_callback_time)} seconds"
                )

    async def _async_callback_wrapper(self):
        self._logger.info("Start callback in cron")
        await self._callback()

    def stop(self):
        self._logger.info("Stopping cron")
        if self._job:
            self._job.cancel()
            self._job = None

    def __str__(self) -> str:
        return f"Cron(expression={self._expression}, timeout={self._timeout}, is_running={self.is_running()})"

    @property
    def expression(self) -> str:
        return self._expression

    @property
    def timeout(self) -> int:
        return self._timeout
