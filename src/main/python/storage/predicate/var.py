import abc
import operator
from typing import Any, Callable

from storage import Var, E, V, Predicate
from storage.predicate import BasePredicate


class Comparison(BasePredicate[Any]):

    def __init__(self, var_a: Var, var_b: Var, op: Callable[[Any, Any], bool]):
        self.var_a = var_a
        self.var_b = var_b
        self.op = op

    def test(self, item: E) -> bool:
        return self.op(self.var_a.value(item), self.var_b.value(item))


class BaseVar(Var[E, V]):

    def __eq__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.eq)

    def __ne__(self, other):
        return Comparison(self, other, operator.ne)

    def __gt__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.gt)

    def __ge__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.ge)

    def __lt__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.lt)

    def __le__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.le)

    def __contains__(self, item: Var) -> Predicate[Any]:
        return Comparison(self, item, operator.contains)

    @abc.abstractmethod
    def value(self, item: E) -> V:
        raise NotImplementedError()


class Const(BaseVar[Any, V]):

    def __init__(self, const: V):
        self.const = const

    def value(self, item: Any) -> V:
        return self.const
