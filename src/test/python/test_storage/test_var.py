from unittest import TestCase

from storage.predicate.jsonpath import JsonPath
from storage.predicate.var import Const


class TestConst(TestCase):

    def test_eq_same_should_be_true(self):
        predicate = Const(1) == Const(1)
        self.assertTrue(predicate.test(None))

    def test_eq_diff_should_be_false(self):
        predicate = Const(1) == Const(2)
        self.assertFalse(predicate.test(None))

    def test_ne_same_should_be_false(self):
        predicate = Const(1) != Const(1)
        self.assertFalse(predicate.test(None))

    def test_ne_diff_should_be_true(self):
        predicate = Const(1) != Const(2)
        self.assertTrue(predicate.test(None))

    def test_gt_true(self):
        predicate = Const(1) > Const(0)
        self.assertTrue(predicate.test(None))

    def test_gt_false(self):
        predicate = Const(1) > Const(2)
        self.assertFalse(predicate.test(None))

    def test_gt_when_equals_should_be_false(self):
        predicate = Const(2) > Const(2)
        self.assertFalse(predicate.test(None))

    def test_ge_true(self):
        predicate = Const(1) >= Const(0)
        self.assertTrue(predicate.test(None))

    def test_ge_false(self):
        predicate = Const(1) >= Const(2)
        self.assertFalse(predicate.test(None))

    def test_ge_when_equals_should_be_true(self):
        predicate = Const(2) >= Const(2)
        self.assertTrue(predicate.test(None))

    def test_lt_true(self):
        predicate = Const(0) < Const(1)
        self.assertTrue(predicate.test(None))

    def test_lt_false(self):
        predicate = Const(2) < Const(1)
        self.assertFalse(predicate.test(None))

    def test_lt_when_equals_should_be_false(self):
        predicate = Const(2) < Const(2)
        self.assertFalse(predicate.test(None))

    def test_le_true(self):
        predicate = Const(0) <= Const(1)
        self.assertTrue(predicate.test(None))

    def test_le_false(self):
        predicate = Const(2) <= Const(1)
        self.assertFalse(predicate.test(None))

    def test_le_when_equals_should_be_true(self):
        predicate = Const(2) <= Const(2)
        self.assertTrue(predicate.test(None))

    def test_mul(self):
        var = Const(2) * Const(3)
        value = var.value(None)
        self.assertEqual(value, 6)

    def test_mul_3(self):
        var = Const(2) * Const(3) * Const(4)
        value = var.value(None)
        self.assertEqual(value, 24)

    def test_truediv(self):
        var = Const(10) / Const(4)
        value = var.value(None)
        self.assertEqual(value, 2.5)

    def test_truediv_3(self):
        var = Const(10) / Const(2) / Const(2)
        value = var.value(None)
        self.assertEqual(value, 2.5)

    def test_add(self):
        var = Const(2) + Const(3)
        value = var.value(None)
        self.assertEqual(value, 5)

    def test_add_3(self):
        var = Const(2) + Const(3) + Const(5)
        value = var.value(None)
        self.assertEqual(value, 10)

    def test_concat(self):
        var = Const('fuu') + Const(' ') + Const('bar')
        value = var.value(None)
        self.assertEqual(value, 'fuu bar')

    def test_sub(self):
        var = Const(2) - Const(3)
        value = var.value(None)
        self.assertEqual(value, -1)

    def test_sub_3(self):
        var = Const(2) - Const(3) - Const(5)
        value = var.value(None)
        self.assertEqual(value, -6)


class TestJsonPath(TestCase):

    def test_(self):
        data = {
            'name': 'Fuu',
            'parents': ['Fuu'],
        }
        predicate = JsonPath.array('$.name') == JsonPath.single('$.parents')
        predicate.test(data)
