import abc
import operator
from functools import reduce, wraps
from typing import Any, Callable, Tuple

from storage import Var, E, V, Predicate


def force_var(func):
    @wraps(func)
    def decorated(self, arg):
        if not isinstance(arg, (Var,)):
            arg = Const(arg)
        return func(self, arg)

    return decorated


class BaseVar(Var[E, V]):

    @force_var
    def __eq__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.eq)

    @force_var
    def __ne__(self, other):
        return Comparison(self, other, operator.ne)

    @force_var
    def __gt__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.gt)

    @force_var
    def __ge__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.ge)

    @force_var
    def __lt__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.lt)

    @force_var
    def __le__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.le)

    @force_var
    def __contains__(self, item: Var) -> Predicate[Any]:
        return Comparison(self, item, operator.contains)

    @force_var
    def __mul__(self, other: Var) -> Var:
        return ReduceArithmetic((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        return ReduceArithmetic((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        return ReduceArithmetic((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        return ReduceArithmetic((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        return ReduceArithmetic((self, power,), operator.pow)

    def __invert__(self) -> Var:
        return NotVar(self)

    @force_var
    def __and__(self, other: Var) -> Var:
        return AndPredicate((self, other,))

    @force_var
    def __or__(self, other: Var) -> Var:
        return OrPredicate((self, other,))

    @abc.abstractmethod
    def __call__(self, item: E) -> V:
        raise NotImplementedError()


class Comparison(BaseVar):

    def __init__(self, var_a: Var, var_b: Var, op: Callable[[Any, Any], bool]):
        self.var_a = var_a
        self.var_b = var_b
        self.op = op

    def __call__(self, item: E) -> bool:
        return self.op(self.var_a(item), self.var_b(item))


class NotVar(BaseVar[E, V]):

    def __init__(self, inner_var: Var[E, V]):
        self.inner_var = inner_var

    def __invert__(self):
        return self.inner_var

    def __call__(self, item: E) -> V:
        return not self.inner_var(item)


class OrPredicate(BaseVar[E, Any]):

    def __init__(self, inner_vars: Tuple[Var[E, Any], ...]):
        self.inner_vars = inner_vars

    @force_var
    def __or__(self, other: Var):
        return OrPredicate(self.inner_vars + (other,))

    def __call__(self, item: E) -> Any:
        for predicate in self.inner_vars:
            val = predicate(item)
            if val:
                return val
        return False


class AndPredicate(BaseVar[E, Any]):
    def __init__(self, inner_vars: Tuple[Var[E, Any], ...]):
        self.inner_vars = inner_vars

    def __and__(self, other: Predicate[E]):
        return AndPredicate(self.inner_vars + (other,))

    def __call__(self, item: E) -> bool:
        for predicate in self.inner_vars:
            if not predicate(item):
                return False
        return True


class ReduceArithmetic(BaseVar[Any, Any]):

    def __init__(self, inner_vars: Tuple[Any, ...], op: Callable[[Any, Any], Any]):
        self.inner_vars = inner_vars
        self.op = op

    @force_var
    def __mul__(self, other: Var) -> Var:
        if self.op == operator.mul:
            return ReduceArithmetic(self.inner_vars + (other,), self.op)
        return ReduceArithmetic((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        if self.op == operator.add:
            return ReduceArithmetic(self.inner_vars + (other,), self.op)
        return ReduceArithmetic((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        if self.op == operator.sub:
            return ReduceArithmetic(self.inner_vars + (other,), self.op)
        return ReduceArithmetic((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        if self.op == operator.truediv:
            return ReduceArithmetic(self.inner_vars + (other,), self.op)
        return ReduceArithmetic((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        if self.op == operator.pow:
            return ReduceArithmetic(self.inner_vars + (power,), self.op)
        return ReduceArithmetic((self, power,), operator.pow)

    def __call__(self, item: E) -> V:
        return reduce(self.op, [var(item) for var in self.inner_vars])


class Const(BaseVar[Any, V]):

    def __init__(self, const: V):
        self.const = const

    def __invert__(self) -> Var:
        return Const(~self.const)

    @force_var
    def __and__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const & other.const)
        return ReduceArithmetic((self, other,), operator.and_)

    @force_var
    def __or__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const | other.const)
        return ReduceArithmetic((self, other,), operator.or_)

    @force_var
    def __mul__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const * other.const)
        return ReduceArithmetic((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const + other.const)
        return ReduceArithmetic((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const - other.const)
        return ReduceArithmetic((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const / other.const)
        return ReduceArithmetic((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        if isinstance(power, (Const,)):
            return Const(self.const / power.const)
        return ReduceArithmetic((self, power,), operator.pow)

    def __call__(self, item: Any = None) -> V:
        return self.const
