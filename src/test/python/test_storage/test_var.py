from unittest import TestCase

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
