import abc
from functools import reduce
from typing import Any, Callable

from storage.api import Set, Var, E


class BaseSet(Set[E]):

    def __and__(self, other: Set[E]) -> Set[E]:
        return ReduceSet((self, other,))

    @abc.abstractmethod
    def __call__(self, item: E) -> E:
        raise NotImplementedError()


class ReduceSet(Set[E]):

    def __init__(self, inner_sets=()):
        self.inner_sets = inner_sets

    def __and__(self, other: Set[E]) -> Set[E]:
        if isinstance(other, ReduceSet):
            return ReduceSet(self.inner_sets + other.inner_sets)
        return ReduceSet(self.inner_sets + (other,))

    def __call__(self, item: E) -> E:
        return reduce(lambda a, b: b(a), self.inner_sets, item)


class FnSet(BaseSet[E]):

    def __init__(self, fn: Callable[[E], E]):
        self.fn = fn

    def __call__(self, item: E) -> E:
        return self.fn(item)


class Sets:

    @staticmethod
    def key(key: str, var: Var[E, Any]) -> Set[E]:
        def set_fn(item: E) -> E:
            item[key] = var(item)
            return item

        return FnSet(set_fn)
