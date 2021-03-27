import abc
import operator
from functools import reduce
from typing import Any, Callable, Tuple

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

    def __mul__(self, other: Var) -> Var:
        return Arithmetic((self, other,), operator.mul)

    def __add__(self, other: Var) -> Var:
        return Arithmetic((self, other,), operator.add)

    def __sub__(self, other: Var) -> Var:
        return Arithmetic((self, other,), operator.sub)

    def __truediv__(self, other: Var) -> Var:
        return Arithmetic((self, other,), operator.truediv)

    @abc.abstractmethod
    def value(self, item: E) -> V:
        raise NotImplementedError()


class Arithmetic(BaseVar[Any, Any]):

    def __init__(self, inner_vars: Tuple[Any, ...], op: Callable[[Any, Any], Any]):
        self.inner_vars = inner_vars
        self.op = op

    def __mul__(self, other: Var) -> Var:
        if self.op == operator.mul:
            return Arithmetic(self.inner_vars + (other,), self.op)
        return Arithmetic((self, other,), operator.mul)

    def __add__(self, other: Var) -> Var:
        if self.op == operator.add:
            return Arithmetic(self.inner_vars + (other,), self.op)
        return Arithmetic((self, other,), operator.add)

    def __sub__(self, other: Var) -> Var:
        if self.op == operator.sub:
            return Arithmetic(self.inner_vars + (other,), self.op)
        return Arithmetic((self, other,), operator.sub)

    def __truediv__(self, other: Var) -> Var:
        if self.op == operator.truediv:
            return Arithmetic(self.inner_vars + (other,), self.op)
        return Arithmetic((self, other,), operator.truediv)

    def value(self, item: E) -> V:
        return reduce(self.op, [var.value(item) for var in self.inner_vars])


class Const(BaseVar[Any, V]):

    def __init__(self, const: V):
        self.const = const

    def __mul__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const * other.const)
        return Arithmetic((self, other,), operator.mul)

    def __add__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const + other.const)
        return Arithmetic((self, other,), operator.add)

    def __sub__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const - other.const)
        return Arithmetic((self, other,), operator.sub)

    def __truediv__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const / other.const)
        return Arithmetic((self, other,), operator.truediv)

    def value(self, item: Any) -> V:
        return self.const
