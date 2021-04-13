from unittest import TestCase
from storage.query.rsql import parse


class RSQLTest(TestCase):

    def test_parse_true_boolean(self):
        rsql = 'true==t'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_parse_false_boolean(self):
        rsql = 'false==f'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_number_symbolic_eq_const_number_when_eq_should_be_true(self):
        rsql = '1==1'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_symbolic_eq_const_when_ne_should_be_false(self):
        rsql = '1==0'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_eq_const_when_eq_should_be_true(self):
        rsql = '1=eq=1'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_eq_const_when_ne_should_be_false(self):
        rsql = '1=eq=0'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_symbolic_ne_const_when_eq_should_be_false(self):
        rsql = '1!=1'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_symbolic_ne_const_when_ne_should_be_true(self):
        rsql = '1!=0'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_ne_const_when_eq_should_be_false(self):
        rsql = '1=ne=1'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_ne_const_when_ne_should_be_true(self):
        rsql = '1=ne=0'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_gt_const_when_gt_should_be_true(self):
        rsql = '1=gt=0'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_gt_const_when_eq_should_be_false(self):
        rsql = '1=gt=1'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_gt_const_when_lt_should_be_false(self):
        rsql = '1=gt=2'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_ge_const_when_gt_should_be_true(self):
        rsql = '1=ge=0'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_ge_const_when_eq_should_be_true(self):
        rsql = '1=ge=1'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_ge_const_when_lt_should_be_false(self):
        rsql = '1=ge=2'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_lt_const_when_lt_should_be_true(self):
        rsql = '0=lt=1'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_lt_const_when_eq_should_be_false(self):
        rsql = '1=lt=1'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_lt_const_when_gt_should_be_false(self):
        rsql = '2=lt=1'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_le_const_when_lt_should_be_true(self):
        rsql = '0=le=1'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_le_const_when_eq_should_be_true(self):
        rsql = '1=le=1'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_le_const_when_gt_should_be_false(self):
        rsql = '2=le=1'
        parsed = parse(rsql)
        self.assertFalse(parsed(None))

    def test_const_in_const_when_in_should_be_true(self):
        rsql = '"a"=in="abc"'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))

    def test_const_contains_const_when_in_should_be_true(self):
        rsql = '"abc"=contains="b"'
        parsed = parse(rsql)
        self.assertTrue(parsed(None))


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
