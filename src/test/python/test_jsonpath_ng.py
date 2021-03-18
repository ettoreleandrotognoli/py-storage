from unittest import TestCase
from jsonpath_ng import parse


class JsonPathNgExampleTest(TestCase):
    jsonpath_expr = parse('foo[*].baz')
    data = {'foo': [{'baz': 1}, {'baz': 2}]}
    values = [1, 2]

    def test_jsonpath(self):
        values = [match.value for match in self.jsonpath_expr.find(self.data)]
        self.assertEqual(values, self.values)
