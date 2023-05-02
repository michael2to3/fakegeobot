import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from bot._user.requestcode import RequestCode
from bot.model import ApiApp, User


class TestRequestCode(unittest.TestCase):
    @patch("bot._user.requestcode.TelegramClient")
    def test_get(self, mock_telegram_client):
        mock_user = MagicMock(spec=User)
        mock_user.session.phone = "+1234567890"
        mock_api = MagicMock(spec=ApiApp)
        mock_api.id = 1234
        mock_api.hash = "abcdefgh"

        mock_client_instance = mock_telegram_client.return_value
        mock_client_instance.connect = AsyncMock()
        mock_send_code_request_result = MagicMock(phone_code_hash="test_hash")
        mock_client_instance.send_code_request = AsyncMock(
            return_value=mock_send_code_request_result
        )

        import asyncio

        result = asyncio.get_event_loop().run_until_complete(
            RequestCode.get(mock_user, mock_api)
        )
        self.assertEqual(result, "test_hash")

        mock_client_instance.connect.assert_called_once()
        mock_client_instance.send_code_request.assert_called_once_with("+1234567890")
