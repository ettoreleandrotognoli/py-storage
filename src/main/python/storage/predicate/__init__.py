import abc
from typing import Callable, Tuple
from storage.api import Predicate, E


class BasePredicate(Predicate[E]):

    def __invert__(self):
        return NotPredicate(self)

    def __or__(self, other: Predicate[E]) -> Predicate[E]:
        return OrPredicate((self, other,))

    def __and__(self, other: Predicate[E]) -> Predicate[E]:
        return AndPredicate((self, other,))

    @abc.abstractmethod
    def test(self, item: E) -> bool:
        raise NotImplementedError()


class NotPredicate(BasePredicate[E]):

    def __init__(self, inner_predicate: Predicate[E]):
        self.inner_predicate = inner_predicate

    def __invert__(self):
        return self.inner_predicate

    def test(self, item: E) -> bool:
        return not self.inner_predicate.test(item)


class OrPredicate(BasePredicate[E]):

    def __init__(self, inner_predicates: Tuple[Predicate[E], ...]):
        self.inner_predicates = inner_predicates

    def __or__(self, other: Predicate[E]):
        return OrPredicate(self.inner_predicates + (other,))

    def test(self, item: E) -> bool:
        for predicate in self.inner_predicates:
            if predicate.test(item):
                return True
        return False


class AndPredicate(BasePredicate[E]):
    def __init__(self, inner_predicates: Tuple[Predicate[E], ...]):
        self.inner_predicates = inner_predicates

    def __and__(self, other: Predicate[E]):
        return AndPredicate(self.inner_predicates + (other,))

    def test(self, item: E) -> bool:
        for predicate in self.inner_predicates:
            if not predicate.test(item):
                return False
        return True


class Func(BasePredicate[E]):

    def __init__(self, func: Callable[[E], bool]):
        self.func = func

    def test(self, item: E) -> bool:
        return self.func(item)

    @classmethod
    def from_lambda(cls, func: Callable[[E], bool]) -> Predicate[E]:
        return cls(func)


class Predicates:
    ANY = Func.from_lambda(lambda _: True)
    NONE = Func.from_lambda(lambda _: False)
