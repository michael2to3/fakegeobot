import asynctest
import asyncio
from unittest.mock import MagicMock
from bot._cron import Cron


class TestCron(asynctest.TestCase):
    async def test_cron(self):
        async def mock_callback():
            return

        expression = "* * * * *"
        timeout = 5

        cron = Cron(mock_callback, expression, timeout)
        self.assertEqual(cron.expression, expression)
        self.assertEqual(cron.timeout, timeout)

        cron.start()
        self.assertTrue(cron.is_running())

        cron.stop()
        self.assertFalse(cron.is_running())

    async def test_cron_callback(self):
        async def mock_callback():
            return

        callback = MagicMock(side_effect=mock_callback)

        cron = Cron(callback, "* * * * * *", 1)
        cron.start()
        await asyncio.sleep(2)
        callback.assert_called()
        cron.stop()

    async def test_avoid_callback_with_timeout(self):
        async def other_mock_callback():
            return

        callback = MagicMock(side_effect=other_mock_callback)

        cron = Cron(callback, "* * * * * *", 10)
        cron.start()
        await asyncio.sleep(5)
        callback.assert_called_once()
        await asyncio.sleep(11)
        self.assertEqual(callback.call_count, 2)
        cron.stop()
