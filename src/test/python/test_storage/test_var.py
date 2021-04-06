from unittest import TestCase

from storage.var.jsonpath import JsonPath
from storage.var import Const, Keys, Vars


class TestConst(TestCase):

    def test_eq_same_should_be_true(self):
        predicate = Const(1) == Const(1)
        self.assertTrue(predicate(None))

    def test_eq_diff_should_be_false(self):
        predicate = Const(1) == Const(2)
        self.assertFalse(predicate(None))

    def test_ne_same_should_be_false(self):
        predicate = Const(1) != Const(1)
        self.assertFalse(predicate(None))

    def test_ne_diff_should_be_true(self):
        predicate = Const(1) != Const(2)
        self.assertTrue(predicate(None))

    def test_gt_true(self):
        predicate = Const(1) > Const(0)
        self.assertTrue(predicate(None))

    def test_gt_false(self):
        predicate = Const(1) > Const(2)
        self.assertFalse(predicate(None))

    def test_gt_when_equals_should_be_false(self):
        predicate = Const(2) > Const(2)
        self.assertFalse(predicate(None))

    def test_ge_true(self):
        predicate = Const(1) >= Const(0)
        self.assertTrue(predicate(None))

    def test_ge_false(self):
        predicate = Const(1) >= Const(2)
        self.assertFalse(predicate(None))

    def test_ge_when_equals_should_be_true(self):
        predicate = Const(2) >= Const(2)
        self.assertTrue(predicate(None))

    def test_lt_true(self):
        predicate = Const(0) < Const(1)
        self.assertTrue(predicate(None))

    def test_lt_false(self):
        predicate = Const(2) < Const(1)
        self.assertFalse(predicate(None))

    def test_lt_when_equals_should_be_false(self):
        predicate = Const(2) < Const(2)
        self.assertFalse(predicate(None))

    def test_le_true(self):
        predicate = Const(0) <= Const(1)
        self.assertTrue(predicate(None))

    def test_le_false(self):
        predicate = Const(2) <= Const(1)
        self.assertFalse(predicate(None))

    def test_le_when_equals_should_be_true(self):
        predicate = Const(2) <= Const(2)
        self.assertTrue(predicate(None))

    def test_mul(self):
        var = Const(2) * Const(3)
        value = var(None)
        self.assertEqual(value, 6)

    def test_mul_3(self):
        var = Const(2) * Const(3) * Const(4)
        value = var(None)
        self.assertEqual(value, 24)

    def test_truediv(self):
        var = Const(10) / Const(4)
        value = var(None)
        self.assertEqual(value, 2.5)

    def test_truediv_3(self):
        var = Const(10) / Const(2) / Const(2)
        value = var(None)
        self.assertEqual(value, 2.5)

    def test_add(self):
        var = Const(2) + Const(3)
        value = var(None)
        self.assertEqual(value, 5)

    def test_add_3(self):
        var = Const(2) + Const(3) + Const(5)
        value = var(None)
        self.assertEqual(value, 10)

    def test_concat(self):
        var = Const('fuu') + Const(' ') + Const('bar')
        value = var(None)
        self.assertEqual(value, 'fuu bar')

    def test_sub(self):
        var = Const(2) - Const(3)
        value = var(None)
        self.assertEqual(value, -1)

    def test_sub_3(self):
        var = Const(2) - Const(3) - Const(5)
        value = var(None)
        self.assertEqual(value, -6)


class TestJsonPath(TestCase):

    def test_(self):
        data = {
            'name': 'Fuu',
            'parents': ['Fuu'],
        }
        predicate = JsonPath.array('$.name') == JsonPath.single('$.parents')
        predicate(data)

    def test_with_op(self):
        data = {
            'name': 'Fuu',
            'height': 1.8,
            'weight': 75.6,
        }
        imc = JsonPath.single('$.weight') / JsonPath.single('$.height') ** Const(2)
        self.assertEqual(imc(data), 75.6 / 1.8 ** 2)

    def test_with_op_and_force_var(self):
        data = {
            'name': 'Fuu',
            'height': 1.8,
            'weight': 75.6,
        }
        imc = JsonPath.single('$.weight') / JsonPath.single('$.height') ** 2
        self.assertEqual(imc(data), 75.6 / 1.8 ** 2)


class TestKeys(TestCase):

    def test_single_key(self):
        id_value = 1
        get_id = Keys(('id',))
        obj = {'id': id_value}
        self.assertEqual(get_id(obj), id_value)

    def test_double_key(self):
        id_value = 1
        get_id = Keys(('parent', 'id',))
        obj = {'parent': {'id': id_value}}
        self.assertEqual(get_id(obj), id_value)


class TestOptimize(TestCase):

    def test_true_or(self):
        var = Vars.const(True) | Vars.key('any')
        optimized_var = var.optimize()
        self.assertTrue(Const.is_true(optimized_var))

    def test_or_true(self):
        var = Vars.key('any') | Vars.const(True)
        optimized_var = var.optimize()
        self.assertTrue(Const.is_true(optimized_var))

    def test_and_false(self):
        var = Vars.key('any') & Vars.const(False)
        optimized_var = var.optimize()
        self.assertTrue(Const.is_false(optimized_var))

    def test_false_and(self):
        var = Vars.const(False) & Vars.key('any')
        optimized_var = var.optimize()
        self.assertTrue(Const.is_false(optimized_var))

    def test_eq_same_key(self):
        var = Vars.key('id') == Vars.key('id')
        optimized_var = var.optimize()
        self.assertTrue(Const.is_true(optimized_var))

    def test_eq_same_keys(self):
        var = Vars.keys(('parent', 'id',)) == Vars.keys(('parent', 'id',))
        optimized_var = var.optimize()
        self.assertTrue(Const.is_true(optimized_var))

    def test_eq_same_const(self):
        var = Vars.const('const') == Vars.const('const')
        optimized_var = var.optimize()
        self.assertTrue(Const.is_true(optimized_var))

    def test_ne_same_key(self):
        var = Vars.key('id') != Vars.key('id')
        optimized_var = var.optimize()
        self.assertTrue(Const.is_false(optimized_var))

    def test_ne_same_keys(self):
        var = Vars.keys(('parent', 'id',)) != Vars.keys(('parent', 'id',))
        optimized_var = var.optimize()
        self.assertTrue(Const.is_false(optimized_var))

    def test_ne_same_const(self):
        var = Vars.const('const') != Vars.const('const')
        optimized_var = var.optimize()
        self.assertTrue(Const.is_false(optimized_var))
