import filecmp
import shutil
import tempfile
from os import path
from unittest import TestCase

from storage.local.file_repository import FileRepository, Serializer
from storage.predicate import Predicates, Vars


class TestReadSingleFileRepository(TestCase):
    sample_content = [
        {"name": "Fuu"},
        {"name": "Bar"}
    ]

    def test_read_sample_json(self):
        file_repository = FileRepository.single_file(
            path.join(path.dirname(__file__), 'single/sample.json'),
            Serializer.json()
        )
        read_sample = list(file_repository.stream())
        self.assertEqual(self.sample_content, read_sample)

    def test_read_sample_toml(self):
        file_repository = FileRepository.single_file(
            path.join(path.dirname(__file__), 'single/sample.toml'),
            Serializer.toml()
        )
        read_sample = list(file_repository.stream())
        self.assertEqual(self.sample_content, read_sample)

    def test_read_sample_yaml(self):
        file_repository = FileRepository.single_file(
            path.join(path.dirname(__file__), 'single/sample.yaml'),
            Serializer.yaml()
        )
        read_sample = list(file_repository.stream())
        self.assertEqual(self.sample_content, read_sample)


class TestWriteSingleFileRepository(TestCase):
    sample_content = [
        {"name": "Fuu"},
        {"name": "Bar"}
    ]

    def test_write_sample_json(self):
        original = path.join(path.dirname(__file__), 'single/sample.json')
        with tempfile.NamedTemporaryFile() as output:
            file_repository = FileRepository.mutable_single_file(
                output.name,
                Serializer.json(),
                Vars.key('name'),
            )
            file_repository.save(self.sample_content)
            self.assertTrue(filecmp.cmp(original, output.name, shallow=False))

    def test_remove_all_json(self):
        original = path.join(path.dirname(__file__), 'single/sample.json')
        with tempfile.NamedTemporaryFile() as output:
            shutil.copy2(original, output.name)
            file_repository = FileRepository.mutable_single_file(
                output.name,
                Serializer.json(),
                Vars.key('name'),
            )
            file_repository.remove(Predicates.ANY)
            content = list(file_repository.stream())
            self.assertEqual(content, [])

    def test_write_sample_yaml(self):
        original = path.join(path.dirname(__file__), 'single/sample.yaml')
        with tempfile.NamedTemporaryFile() as output:
            file_repository = FileRepository.mutable_single_file(
                output.name,
                Serializer.yaml(),
                Vars.key('name'),
            )
            file_repository.save(self.sample_content)
            self.assertTrue(filecmp.cmp(original, output.name, shallow=False))

    def test_remove_all_yaml(self):
        original = path.join(path.dirname(__file__), 'single/sample.yaml')
        with tempfile.NamedTemporaryFile() as output:
            shutil.copy2(original, output.name)
            file_repository = FileRepository.mutable_single_file(
                output.name,
                Serializer.yaml(),
                Vars.key('name'),
            )
            file_repository.remove(Predicates.ANY)
            content = list(file_repository.stream())
            self.assertEqual(content, [])

    def test_write_sample_toml(self):
        original = path.join(path.dirname(__file__), 'single/sample.toml')
        with tempfile.NamedTemporaryFile() as output:
            file_repository = FileRepository.mutable_single_file(
                output.name,
                Serializer.toml(),
                Vars.key('name'),
            )
            file_repository.save(self.sample_content)
            self.assertTrue(filecmp.cmp(original, output.name, shallow=False))

    def test_remove_all_toml(self):
        original = path.join(path.dirname(__file__), 'single/sample.toml')
        with tempfile.NamedTemporaryFile() as output:
            shutil.copy2(original, output.name)
            file_repository = FileRepository.mutable_single_file(
                output.name,
                Serializer.toml(),
                Vars.key('name'),
            )
            file_repository.remove(Predicates.ANY)
            content = list(file_repository.stream())
            self.assertEqual(content, [])
