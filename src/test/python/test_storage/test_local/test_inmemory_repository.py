from unittest import TestCase

from storage.local.inmemory_repository import InMemoryRepository
from storage.var import Vars
from storage.predicate import Predicates
from storage.setter import Setters


class TestInMemoryRepository(TestCase):
    sample_content = [
        {"name": "Fuu"},
        {"name": "Bar"}
    ]

    def test_read_sample(self):
        file_repository = InMemoryRepository(
            pk_factory=Vars.key('name'),
            initial_data=self.sample_content,
        )
        read_sample = list(file_repository.stream())
        self.assertEqual(read_sample, self.sample_content)

    def test_write_sample(self):
        file_repository = InMemoryRepository(
            pk_factory=Vars.key('name'),
        )
        file_repository.save(self.sample_content)
        read_sample = list(file_repository.stream())
        self.assertEqual(read_sample, self.sample_content)

    def test_remove_all(self):
        file_repository = InMemoryRepository(
            pk_factory=Vars.key('name'),
            initial_data=self.sample_content,
        )
        file_repository.remove(Predicates.ANY)
        read_sample = list(file_repository.stream())
        self.assertEqual(read_sample, [])

    def test_clear(self):
        file_repository = InMemoryRepository(
            pk_factory=Vars.key('name'),
            initial_data=self.sample_content,
        )
        file_repository.clear()
        read_sample = list(file_repository.stream())
        self.assertEqual(read_sample, [])

    def test_predicate(self):
        file_repository = InMemoryRepository(
            pk_factory=Vars.key('name'),
            initial_data=self.sample_content,
        )
        read_sample = list(file_repository.stream(Vars.key("name") == "Fuu"))
        self.assertEqual(read_sample, [self.sample_content[0]])

    def test_update_all(self):
        file_repository = InMemoryRepository(
            pk_factory=Vars.key('name'),
            initial_data=self.sample_content,
        )
        file_repository.update(
            Setters.key('name', Vars.const('Updated ') + Vars.key('name')),
        )
