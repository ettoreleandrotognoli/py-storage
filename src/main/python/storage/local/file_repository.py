import abc
from string import Formatter
import glob
import os
from dataclasses import dataclass
from typing import Iterator, Callable, Hashable, Iterable, Dict, Any, TextIO

from storage import E, Generic
from storage.api import MutableRepository, Predicate, Repository
from storage.predicate import Predicates, Vars
from storage.serializer import Serializer


class FileStrategy(Generic[E]):

    @abc.abstractmethod
    def file_for(self, item: E) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def file_stream(self) -> Iterable[str]:
        raise NotImplementedError()

    def group_by_file(self, bunch: Iterable[E]) -> Dict[str, Iterable[E]]:
        items_peer_files = {}
        for item in bunch:
            file_name = self.file_for(item)
            items_peer_files[file_name] = items_peer_files.get(file_name, []) + [item]
        return items_peer_files


class SerializeStrategy(Generic[E]):
    @abc.abstractmethod
    def read(self, input_stream: TextIO) -> Iterator[E]:
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, output_stream: TextIO, bunch: Iterable[E]):
        raise NotImplementedError()


class SingleFileStrategy(FileStrategy[E]):

    def __init__(self, file_name: str):
        self.file_name = file_name

    def file_stream(self) -> Iterable[str]:
        return [self.file_name]

    def file_for(self, item: E) -> str:
        return self.file_name

    def group_by_file(self, bunch: Iterable[E]) -> Dict[str, Iterable[E]]:
        return {self.file_name: bunch}


class MultipleFileStrategy(FileStrategy[E]):

    def __init__(self, file_name_template: str, args_factories: Dict[str, Callable[[E], Any]]):
        self.file_name_template = file_name_template
        self.args_factories = args_factories

    def template_args(self, item: E) -> dict:
        return dict((k, v(item),) for k, v in self.args_factories.items())

    def template_glob_args(self):
        return dict((k, '*',) for k, v in self.args_factories.items())

    def file_for(self, item: E) -> str:
        return self.file_name_template.format(**self.template_args(item))

    def file_stream(self) -> Iterable[str]:
        return glob.glob(self.file_name_template.format(**self.template_glob_args()))


def default_args_factory(template: str) -> Dict[str, Callable[[Any], Any]]:
    formatter = Formatter()
    parsed = formatter.parse(template)
    keys = [key for prefix, key, _, _ in parsed if key is not None]
    return dict((k, Vars.key(k),) for k in keys)


class ManyPerFileStrategy(SerializeStrategy[E]):

    def __init__(self, serializer: Serializer[E]):
        self.serializer = serializer

    def read(self, input_stream: TextIO) -> Iterator[E]:
        return self.serializer.read_many(input_stream)

    def write(self, output_stream: TextIO, bunch: Iterable[E]):
        self.serializer.write_many(output_stream, bunch)


class OnePerFileStrategy(SerializeStrategy[E]):
    def __init__(self, serializer: Serializer[E]):
        self.serializer = serializer

    def read(self, input_stream: TextIO) -> Iterator[E]:
        return [self.serializer.read_one(input_stream)]

    def write(self, output_stream: TextIO, bunch: Iterable[E]):
        self.serializer.write_one(output_stream, next(iter(bunch)))


class FileRepository(MutableRepository[E]):
    class Strategy(SerializeStrategy[E], FileStrategy[E]):
        @abc.abstractmethod
        def pk_for(self, item: E) -> Hashable:
            raise NotImplementedError()

    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def file_to_stream(self, file_name: str, predicate: Predicate[E] = None) -> Iterator[E]:
        try:
            with open(file_name) as input_stream:
                yield from filter(predicate, self.strategy.read(input_stream))
        except ValueError as ex:
            if os.path.getsize(file_name) == 0:
                return []
            raise ex
        except Exception as _:
            return []

    def stream(self, predicate: Predicate[E] = Predicates.ANY) -> Iterator[E]:
        for file_name in self.strategy.file_stream():
            yield from self.file_to_stream(file_name, predicate)

    def save(self, bunch: Iterator[E]):
        items_per_files = self.strategy.group_by_file(bunch)
        for file_name in items_per_files.keys():
            bunch = items_per_files[file_name]
            data = dict((self.strategy.pk_for(item), item,) for item in self.file_to_stream(file_name))
            for item in bunch:
                identifier = self.strategy.pk_for(item)
                data[identifier] = item
            with open(file_name, 'w+') as output_stream:
                self.strategy.write(output_stream, [v for v in data.values()])

    def remove(self, predicate: Predicate[E]):
        keep = ~predicate
        for file_name in self.strategy.file_stream():
            with open(file_name, 'w+') as output_stream:
                keep_data = filter(keep, self.file_to_stream(file_name))
                self.strategy.write(output_stream, [v for v in keep_data])

    def clear(self):
        for file_name in self.strategy.file_stream():
            os.remove(file_name)

    @classmethod
    def single_file(cls, file_name: str, serializer: Serializer[E]) -> Repository[E]:
        strategy = ComposedStrategy(
            file_strategy=SingleFileStrategy(file_name),
            serialize_strategy=ManyPerFileStrategy(serializer),
            pk_factory=None,
        )
        return FileRepository(strategy)

    @classmethod
    def mutable_single_file(cls,
                            file_name: str,
                            serializer: Serializer[E],
                            pk_factory: Callable[[E], Hashable]) -> MutableRepository[E]:
        strategy = ComposedStrategy(
            file_strategy=SingleFileStrategy(file_name),
            serialize_strategy=ManyPerFileStrategy(serializer),
            pk_factory=pk_factory,
        )
        return FileRepository(strategy)

    @classmethod
    def one_per_file(cls,
                     template: str,
                     serializer: Serializer[E]) -> Repository[E]:
        strategy = ComposedStrategy(
            file_strategy=MultipleFileStrategy(template, default_args_factory(template)),
            serialize_strategy=OnePerFileStrategy(serializer),
            pk_factory=None,
        )
        return FileRepository(strategy)

    @classmethod
    def mutable_one_per_file(cls,
                             template: str,
                             serializer: Serializer[E],
                             pk_factory: Callable[[E], Hashable]) -> MutableRepository[E]:
        strategy = ComposedStrategy(
            file_strategy=MultipleFileStrategy(template, default_args_factory(template)),
            serialize_strategy=OnePerFileStrategy(serializer),
            pk_factory=pk_factory,
        )
        return FileRepository(strategy)

    @classmethod
    def multiple_file(cls,
                      template: str,
                      serializer: Serializer[E]) -> Repository[E]:
        strategy = ComposedStrategy(
            file_strategy=MultipleFileStrategy(template, default_args_factory(template)),
            serialize_strategy=ManyPerFileStrategy(serializer),
            pk_factory=None,
        )
        return FileRepository(strategy)

    @classmethod
    def mutable_multiple_file(cls,
                              template: str,
                              serializer: Serializer[E],
                              pk_factory: Callable[[E], Hashable]) -> MutableRepository[E]:
        strategy = ComposedStrategy(
            file_strategy=MultipleFileStrategy(template, default_args_factory(template)),
            serialize_strategy=ManyPerFileStrategy(serializer),
            pk_factory=pk_factory,
        )
        return FileRepository(strategy)


@dataclass()
class ComposedStrategy(FileRepository.Strategy[E]):
    file_strategy: FileStrategy
    serialize_strategy: SerializeStrategy
    pk_factory: Callable[[E], Hashable]

    def file_for(self, item: E) -> str:
        return self.file_strategy.file_for(item)

    def file_stream(self) -> Iterable[str]:
        return self.file_strategy.file_stream()

    def group_by_file(self, bunch: Iterable[E]) -> Dict[str, Iterable[E]]:
        return self.file_strategy.group_by_file(bunch)

    def read(self, input_stream: TextIO) -> Iterator[E]:
        return self.serialize_strategy.read(input_stream)

    def write(self, output_stream: TextIO, bunch: Iterator[E]):
        return self.serialize_strategy.write(output_stream, bunch)

    def pk_for(self, item: E) -> Hashable:
        return self.pk_factory(item)
