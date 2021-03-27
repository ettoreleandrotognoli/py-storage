from __future__ import annotations
import abc
from typing import Generic, TypeVar, Type, Iterator

E = TypeVar('E')
V = TypeVar('V')


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


class Var(Generic[E, V]):

    @abc.abstractmethod
    def __eq__(self, other: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __ne__(self, other: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __gt__(self, other: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __ge__(self, other: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __lt__(self, other: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __le__(self, other: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __contains__(self, item: Var) -> Predicate:
        raise NotImplementedError()

    @abc.abstractmethod
    def __mul__(self, other: Var) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __add__(self, other: Var) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __sub__(self, other: Var) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __truediv__(self, other: Var) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def value(self, item: E) -> V:
        raise NotImplementedError()

