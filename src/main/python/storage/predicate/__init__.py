from __future__ import annotations

from typing import Callable

from storage.api import Predicate, E
from storage.predicate.var import BaseVar


class Func(BaseVar):

    def __init__(self, func: Callable[[E], bool]):
        self.func = func

    def __call__(self, item: E) -> bool:
        return self.func(item)

    @classmethod
    def from_lambda(cls, func: Callable[[E], bool]) -> Predicate[E]:
        return cls(func)


class Predicates:
    ANY = Func.from_lambda(lambda _: True)
    NONE = Func.from_lambda(lambda _: False)
