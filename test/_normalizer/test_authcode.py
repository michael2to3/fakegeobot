import unittest

from bot._normalizer.auth_code import AuthCode


class TestAuthCode(unittest.TestCase):

    def test_normalize_valid_code(self):
        input_text = "Your code is 12345."
        expected_output = "12345"
        result = AuthCode.normalize(input_text)
        self.assertEqual(result, expected_output)

    def test_normalize_invalid_code_with_non_digit(self):
        input_text = "Your code is 12a45."
        with self.assertRaises(ValueError) as context:
            AuthCode.normalize(input_text)

        self.assertEqual(str(context.exception), "Auth code has not allow symbol")

    def test_normalize_invalid_code_with_wrong_length(self):
        input_text = "Your code is 123456."
        with self.assertRaises(ValueError) as context:
            AuthCode.normalize(input_text)

        self.assertEqual(str(context.exception), "Not correct code")

    def test__bypass_protect_tg(self):
        input_text = "123.45"
        expected_output = "12345"
        result = AuthCode._bypass_protect_tg(input_text)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
