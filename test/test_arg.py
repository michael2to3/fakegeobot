import unittest
from rootpath import fakegeo

Arg = fakegeo.Arg


class ArgTest(unittest.TestCase):
    _arg = Arg()

    def test_get_phone_number(self):
        text = "/some_cmd +78005553535"
        phone = self._arg.get_phone(text)
        self.assertEqual(phone, "+78005553535")

        text = "/some_cmd 88005553535"
        phone = self._arg.get_phone(text)
        self.assertEqual(phone, "88005553535")

        text = "/some_cmd 8 800 555 3535"
        phone = self._arg.get_phone(text)
        self.assertEqual(phone, "88005553535")

        text = "/some_cmd 8+800 555 3535"
        self.assertRaises(ValueError, self._arg.get_phone, text)

        text = "/some_cmd 8(800)555 3535"
        phone = self._arg.get_phone(text)
        self.assertEqual(phone, "88005553535")

        text = "/some_cmd 8(800)555_3535"
        phone = self._arg.get_phone(text)
        self.assertEqual(phone, "88005553535")

        text = " 88005553535"
        phone = self._arg.get_phone(text)
        self.assertEqual(phone, "88005553535")

    def test_get_auth_code(self):
        text = "/some_cmd 76481"
        code = self._arg.get_auth_code(text)
        self.assertEqual(code, 76481)

        text = "76481"
        code = self._arg.get_auth_code(text)
        self.assertEqual(code, 76481)

        text = " 76481"
        code = self._arg.get_auth_code(text)
        self.assertEqual(code, 76481)

        text = "/asd 76481 asd"
        self.assertRaises(ValueError, self._arg.get_auth_code, text)

        text = "/asd 764810   "
        self.assertRaises(ValueError, self._arg.get_auth_code, text)

        text = "/asd 7648"
        self.assertRaises(ValueError, self._arg.get_auth_code, text)

        text = "/asd 2.7.5.0.5"
        self.assertEqual(self._arg.get_auth_code(text), 27505)

    def test_schedule(self):
        ptext = "30 18 * * 6"
        self.assertEqual(self._arg.get_cron(ptext), ptext)
        text = "/cmd 30 18 * * 6"
        self.assertEqual(self._arg.get_cron(text), ptext)
        text = "18 * * 6"
        self.assertRaises(ValueError, self._arg.get_cron, text)
