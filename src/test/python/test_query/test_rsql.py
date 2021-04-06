from unittest import TestCase
from storage.query.rsql import parse


class RSQLTest(TestCase):

    def test_parse_id_eq_1(self):
        rsql = 'id==1'
        parsed = parse(rsql)
        self.assertTrue(parsed({'id': 1}))

    def test_parse_id_eq_1_and_name_eq_literal_test(self):
        rsql = 'id==1&name=="test"'
        parsed = parse(rsql)
        self.assertTrue(parsed({'id': 1, 'name': 'test'}))

    def test_parse_precedence(self):
        rsql = 'id==1|name=="test"&id!=1'
        parsed = parse(rsql)
        self.assertTrue(parsed({'id': 1, 'name': 'test'}))

    def test_parse_array(self):
        rsql = 'children==[1,"a",3.1]'
        parsed = parse(rsql)
        self.assertTrue(parsed({'children': (1, 'a', 3.1)}))
