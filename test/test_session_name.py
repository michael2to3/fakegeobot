from rootpath import fakegeo
import unittest

SessionName = fakegeo.SessionName


class SessionNameTest(unittest.TestCase):
    _name = SessionName()

    def test_check_random(self):
        lhs = self._name.get_session_name()
        rhs = self._name.get_session_name()
        self.assertNotEqual(lhs, rhs)

    def test_check_hash(self):
        base = self._name.get_session_name()
        lhs = self._name.get_session_name_base(base)
        rhs = self._name.get_session_name_base(base)
        self.assertEqual(lhs, rhs)
        base = self._name.get_session_name()
        rhs = self._name.get_session_name_base(base)
        self.assertNotEqual(lhs, rhs)
