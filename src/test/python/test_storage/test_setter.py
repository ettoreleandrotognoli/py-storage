from unittest import TestCase

from storage.var import Vars
from storage.setter import Setters


class TestSet(TestCase):

    def test_set_with_const(self):
        expected = {'a': 2}
        obj = {'a': 1}
        setter = Setters.key('a', Vars.const(2))
        result = setter(obj)
        self.assertEqual(result, expected)

    def test_set_and(self):
        expected = {
            'a': 2,
            'b': 3,
        }
        obj = {
            'a': 1
        }
        setter = Setters.key('a', Vars.const(2)) & Setters.key('b', Vars.const(3))
        result = setter(obj)
        self.assertEqual(result, expected)

    def test_set_with_dynamic(self):
        expected = {
            'a': 2,
            'b': 1,
        }
        obj = {
            'a': 1
        }
        setter = Setters.key('b', Vars.key('a')) & Setters.key('a', Vars.const(2))
        result = setter(obj)
        self.assertEqual(result, expected)
