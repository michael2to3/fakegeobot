import unittest
from bot._normalizer.phonenumber import PhoneNumber


class TestPhoneNumber(unittest.TestCase):
    def test_normalize(self):
        valid_phones = [
            "+1234567890",
            "1234567890",
            "(123) 456-7890",
            "+1 234-567_890",
            "1(234) 567 890",
        ]
        for phone in valid_phones:
            self.assertEqual(PhoneNumber.normalize(phone), "+1234567890", phone)

        invalid_char_phones = [
            "12345a67890",
            "+1234&567890",
            "12@34567890",
        ]
        for phone in invalid_char_phones:
            self.assertEqual(PhoneNumber.normalize(phone), "+1234567890", phone)

        invalid_length_phones = [
            "+123456789",
            "12345678901234",
        ]
        for phone in invalid_length_phones:
            with self.assertRaises(ValueError, msg="Phone format is not valid"):
                PhoneNumber.normalize(phone)
