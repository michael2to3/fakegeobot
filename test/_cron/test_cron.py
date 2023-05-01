import asyncio
import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock
from bot._cron import Cron, FloodException


class TestCron(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.callback = AsyncMock()
        self.expression = "0 0 * * *"
        self.timeout = 60
        self.cron = Cron(self.callback, self.expression, self.timeout)

    async def test_validate_expression(self):
        with self.assertRaises(ValueError):
            Cron(self.callback, "*/15", self.timeout)

        with self.assertRaises(FloodException):
            Cron(self.callback, "* * * * *", self.timeout)

        with self.assertRaises(FloodException):
            Cron(self.callback, "*/1 * * * *", self.timeout)

    async def test_start_and_stop(self):
        self.assertFalse(self.cron.is_running())
        self.cron.start()
        self.assertTrue(self.cron.is_running())
        self.cron.stop()
        self.assertFalse(self.cron.is_running())

    async def test_schedule_runner(self):
        self.cron.start()
        await asyncio.sleep(3)
        self.callback.assert_called_once()
        self.cron.stop()

    async def test_str_representation(self):
        cron_repr = str(self.cron)
        self.assertIn("expression", cron_repr)
        self.assertIn("timeout", cron_repr)
        self.assertIn("is_running", cron_repr)


if __name__ == "__main__":
    unittest.main()
