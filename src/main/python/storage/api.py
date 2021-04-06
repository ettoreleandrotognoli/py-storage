from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, Iterator, Callable

E = TypeVar('E')
V = TypeVar('V')


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
    def __pow__(self, power, modulo=None) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __invert__(self) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __and__(self, other: Var) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __or__(self, other: Var) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def cast(self, cast_fn: Callable) -> Var:
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, item: E) -> V:
        raise NotImplementedError()


class Set(Generic[E]):

    @abc.abstractmethod
    def __and__(self, other: Set[E]) -> Set[E]:
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, item: E) -> E:
        raise NotImplementedError()


Predicate = Var[E, bool]


class Storage(abc.ABC):

    @abc.abstractmethod
    def repository_for(self, item_type: Type[E]) -> Repository[E]:
        raise NotImplementedError()


class MutableStorage(Storage):

    @abc.abstractmethod
    def mutable_repository_for(self, item_type: Type[E]) -> MutableRepository[E]:
        raise NotImplementedError()


class MutableStorageSession(MutableStorage):

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()


class SessionSupportStorage(MutableStorage):

    @abc.abstractmethod
    def open_session(self, message=None) -> MutableStorageSession:
        raise NotImplementedError()


class Repository(Generic[E]):

    @abc.abstractmethod
    def stream(self, predicate: Predicate[E] = None) -> Iterator[E]:
        raise NotImplementedError()


class MutableRepository(Repository[E]):
    @abc.abstractmethod
    def save(self, bunch: Iterator[E]):
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, update_fn: Callable[[E], E], predicate: Predicate[E] = None):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, predicate: Predicate[E]):
        raise NotImplementedError()

    @abc.abstractmethod
    def clear(self):
        raise NotImplementedError()
