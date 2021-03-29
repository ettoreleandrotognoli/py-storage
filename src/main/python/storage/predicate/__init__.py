from __future__ import annotations

from typing import Callable, Sequence

from storage.api import Predicate, E
from storage.predicate.var import BaseVar, Const


class Func(BaseVar):

    def __init__(self, func: Callable[[E], bool]):
        self.func = func

    def __call__(self, item: E) -> bool:
        return self.func(item)

    @classmethod
    def from_lambda(cls, func: Callable[[E], bool]) -> Predicate[E]:
        return cls(func)


class Predicates:
    ANY = Const(True)
    NONE = Const(False)


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
