import asyncio
import logging
import time
from typing import Any, Callable, Coroutine
from croniter import croniter


class Cron:
    __slots__ = (
        "_logger",
        "_callback",
        "_cron_expression",
        "_callback_timeout",
        "_running_task",
        "_last_callback_time_seconds",
    )

    _logger: logging.Logger
    _callback: Callable[[], Coroutine[Any, Any, None]]
    _cron_expression: str
    _callback_timeout: int
    _running_task: Any
    _last_callback_time_seconds: float

    def __init__(
        self,
        callback: Callable[[], Coroutine[Any, Any, None]],
        cron_expression: str,
        callback_timeout: int,
    ):
        self._logger = logging.getLogger(__name__)
        self._callback = callback
        self._cron_expression = cron_expression
        self._callback_timeout = callback_timeout
        self._running_task = None
        self._last_callback_time_seconds = 0

    def start(self) -> None:
        self._logger.info("Starting cron")
        if self._running_task is None:
            self._running_task = asyncio.ensure_future(self._schedule_runner())

    def is_running(self) -> bool:
        return self._running_task is not None

    async def _schedule_runner(self):
        cron_iter = croniter(self._cron_expression, time.time())
        while True:
            next_run = cron_iter.get_next(float)
            await asyncio.sleep(next_run - time.time())
            current_time = time.time()
            if (
                current_time - self._last_callback_time_seconds
                >= self._callback_timeout
            ):
                self._logger.info("Scheduling callback")
                self._last_callback_time_seconds = current_time
                try:
                    await self._async_callback_wrapper()
                except Exception as e:
                    self._logger.error(f"Error in callback: {e}")
            else:
                self._logger.info("Scheduling next run")

    async def _async_callback_wrapper(self):
        self._logger.info("Start callback in cron")
        await self._callback()

    def stop(self) -> None:
        self._logger.info("Stopping cron")
        if self._running_task:
            self._running_task.cancel()
            self._running_task = None

    def __str__(self) -> str:
        return f"Cron(expression={self._cron_expression}, timeout={self._callback_timeout}, is_running={self.is_running()})"

    def __del__(self):
        self.stop()

    @property
    def expression(self) -> str:
        return self._cron_expression

    @property
    def timeout(self) -> int:
        return self._callback_timeout
