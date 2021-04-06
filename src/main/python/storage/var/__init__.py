from __future__ import annotations

import abc
import operator
from functools import reduce, wraps
from typing import Callable, Sequence, Any
from typing import Tuple

from storage import V
from storage.api import Predicate, E, Var


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
        return ReduceOperator((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        return ReduceOperator((self, power,), operator.pow)

    def __invert__(self) -> Var:
        return NotOperator(self)

    @force_var
    def __and__(self, other: Var) -> Var:
        return AndOperator((self, other,))

    @force_var
    def __or__(self, other: Var) -> Var:
        return OrOperator((self, other,))

    def cast(self, cast_fn: Callable):
        return CastOperator(cast_fn, self)

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


class CastOperator(BaseVar[E, V]):

    def __init__(self, cast_fn: Callable[[Any], V], inner_var: Var[E, Any]):
        self.cast_fn = cast_fn
        self.inner_var = inner_var

    def __call__(self, item: E) -> V:
        return self.cast_fn(self.inner_var(item))

    def cast(self, cast_fn: Callable):
        if self.cast_fn == cast_fn:
            return self
        return CastOperator(cast_fn, self)


class NotOperator(BaseVar[E, V]):

    def __init__(self, inner_var: Var[E, V]):
        self.inner_var = inner_var

    def __invert__(self):
        return self.inner_var

    def __call__(self, item: E) -> V:
        return not self.inner_var(item)


class OrOperator(BaseVar[E, Any]):

    def __init__(self, inner_vars: Tuple[Var[E, Any], ...]):
        self.inner_vars = inner_vars

    @force_var
    def __or__(self, other: Var):
        return OrOperator(self.inner_vars + (other,))

    def __call__(self, item: E) -> Any:
        for predicate in self.inner_vars:
            val = predicate(item)
            if val:
                return val
        return False


class AndOperator(BaseVar[E, Any]):
    def __init__(self, inner_vars: Tuple[Var[E, Any], ...]):
        self.inner_vars = inner_vars

    def __and__(self, other: Predicate[E]):
        return AndOperator(self.inner_vars + (other,))

    def __call__(self, item: E) -> bool:
        for predicate in self.inner_vars:
            if not predicate(item):
                return False
        return True


class ReduceOperator(BaseVar[Any, Any]):

    def __init__(self, inner_vars: Tuple[Any, ...], op: Callable[[Any, Any], Any]):
        self.inner_vars = inner_vars
        self.op = op

    @force_var
    def __mul__(self, other: Var) -> Var:
        if self.op == operator.mul:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        if self.op == operator.add:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        if self.op == operator.sub:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        if self.op == operator.truediv:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        if self.op == operator.pow:
            return ReduceOperator(self.inner_vars + (power,), self.op)
        return ReduceOperator((self, power,), operator.pow)

    def __call__(self, item: E) -> V:
        return reduce(self.op, [var(item) for var in self.inner_vars])


class Const(BaseVar[Any, V]):

    def __init__(self, const: V):
        self.const = const

    def __invert__(self) -> Var:
        return Const(not self.const)

    @force_var
    def __and__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const & other.const)
        return ReduceOperator((self, other,), operator.and_)

    @force_var
    def __or__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const | other.const)
        return ReduceOperator((self, other,), operator.or_)

    @force_var
    def __mul__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const * other.const)
        return ReduceOperator((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const + other.const)
        return ReduceOperator((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const - other.const)
        return ReduceOperator((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const / other.const)
        return ReduceOperator((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        if isinstance(power, (Const,)):
            return Const(self.const ** power.const)
        return ReduceOperator((self, power,), operator.pow)

    def cast(self, cast_fn: Callable):
        if isinstance(cast_fn, (type,)) and isinstance(self.const, cast_fn):
            return self
        return CastOperator(cast_fn, self)

    def __call__(self, item: Any = None) -> V:
        return self.const


class Func(BaseVar):

    def __init__(self, func: Callable[[E], bool]):
        self.func = func

    def __call__(self, item: E) -> bool:
        return self.func(item)

    @classmethod
    def from_lambda(cls, func: Callable[[E], bool]) -> Predicate[E]:
        return cls(func)


class Vars:

    @staticmethod
    def key(key: str):
        return Func.from_lambda(lambda it: it.get(key, None))

    @staticmethod
    def keys(keys: Sequence[str]):
        def get(item: dict):
            for key in keys and item is not None:
                item = item.get(key, None)
            return item

        return Func.from_lambda(get)

    @staticmethod
    def const(value: E) -> Var[Any, E]:
        return Const(value)
