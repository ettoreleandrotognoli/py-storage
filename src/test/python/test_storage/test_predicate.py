from unittest import TestCase

from storage.predicate import Predicates


class TestPredicate(TestCase):

    def test_any(self):
        predicate = Predicates.ANY
        self.assertTrue(predicate(None))

    def test_not_any(self):
        predicate = ~Predicates.ANY
        self.assertFalse(predicate(None))

    def test_any_and_any(self):
        predicate = Predicates.ANY & Predicates.ANY
        self.assertTrue(predicate(None))

    def test_any_or_any(self):
        predicate = Predicates.ANY | Predicates.ANY
        self.assertTrue(predicate(None))

    def test_none(self):
        predicate = Predicates.NONE
        self.assertFalse(predicate(None))

    def test_not_none(self):
        predicate = ~Predicates.NONE
        self.assertTrue(predicate(None))

    def test_none_and_none(self):
        predicate = Predicates.NONE & Predicates.NONE
        self.assertFalse(predicate(None))

    def test_none_or_none(self):
        predicate = Predicates.NONE | Predicates.NONE
        self.assertFalse(predicate(None))

    def test_any_and_none(self):
        predicate = Predicates.ANY & Predicates.NONE
        self.assertFalse(predicate(None))

    def test_any_or_none(self):
        predicate = Predicates.ANY | Predicates.NONE
        self.assertTrue(predicate(None))
