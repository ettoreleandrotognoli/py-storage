from typing import Iterable, Iterator, Callable, Hashable

from storage import MutableRepository, E, Predicate


class InMemoryRepository(MutableRepository[E]):

    def __init__(self, pk_factory: Callable[[E], Hashable], content_initializer=dict, initial_data: Iterable[E] = None):
        self.content_initializer = content_initializer
        self.content = self.content_initializer()
        self.pk_factory = pk_factory
        self.save(initial_data or [])

    def stream(self, predicate: Predicate[E] = None) -> Iterator[E]:
        return iter(filter(predicate, self.content.values()))

    def save(self, bunch: Iterator[E]):
        for item in bunch:
            pk = self.pk_factory(item)
            self.content[pk] = item

    def remove(self, predicate: Predicate[E]):
        keep = ~predicate
        self.content = dict((self.pk_factory(k), v,) for k, v in self.content.items() if keep(v))

    def clear(self):
        self.content = self.content_initializer()
