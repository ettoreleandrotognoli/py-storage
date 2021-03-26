from __future__ import annotations
import abc
from typing import Generic, TypeVar, Type, Iterator

E = TypeVar('E')


class Predicate(Generic[E]):
    @abc.abstractmethod
    def test(self, item: E) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def __invert__(self) -> Predicate[E]:
        raise NotImplementedError()

    @abc.abstractmethod
    def __or__(self, other: Predicate[E]) -> Predicate[E]:
        raise NotImplementedError()

    @abc.abstractmethod
    def __and__(self, other: Predicate[E]) -> Predicate[E]:
        raise NotImplementedError()
