from unittest import TestCase

from storage.var import Vars
from storage.set import Sets


class TestSet(TestCase):

    def test_set_with_const(self):
        expected = {'a': 2}
        obj = {'a': 1}
        set = Sets.key('a', Vars.const(2))
        result = set(obj)
        self.assertEqual(result, expected)

    def test_set_and(self):
        expected = {
            'a': 2,
            'b': 3,
        }
        obj = {
            'a': 1
        }
        set = Sets.key('a', Vars.const(2)) & Sets.key('b', Vars.const(3))
        result = set(obj)
        self.assertEqual(result, expected)

    def test_set_with_dynamic(self):
        expected = {
            'a': 2,
            'b': 1,
        }
        obj = {
            'a': 1
        }
        set = Sets.key('b', Vars.key('a')) & Sets.key('a', Vars.const(2))
        result = set(obj)
        self.assertEqual(result, expected)
