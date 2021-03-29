import tempfile
import filecmp
from os import path
from unittest import TestCase

from storage.local.file_repository import FileRepository
from storage.predicate import Vars
from storage.serializer import Serializer


class TestReadOnePerFileRepository(TestCase):
    sample_content = [
        {'name': 'java'},
        {'name': 'python'}
    ]

    def test_read_sample_yml(self):
        file_repository = FileRepository.one_per_file(
            path.join(path.dirname(__file__), 'multiple/by-name/{name}.yml'),
            Serializer.yaml()
        )
        read_sample = sorted(list(file_repository.stream()), key=Vars.key('name'))
        self.assertEqual(read_sample, self.sample_content)

    def test_read_sample_json(self):
        file_repository = FileRepository.one_per_file(
            path.join(path.dirname(__file__), 'multiple/by-name/{name}.json'),
            Serializer.json()
        )
        read_sample = sorted(list(file_repository.stream()), key=Vars.key('name'))
        self.assertEqual(read_sample, self.sample_content)

    def test_read_sample_toml(self):
        file_repository = FileRepository.one_per_file(
            path.join(path.dirname(__file__), 'multiple/by-name/{name}.toml'),
            Serializer.toml()
        )
        read_sample = sorted(list(file_repository.stream()), key=Vars.key('name'))
        self.assertEqual(read_sample, self.sample_content)

    def test_write_sample_json(self):
        original = path.join(path.dirname(__file__), 'multiple/by-name/')
        with tempfile.TemporaryDirectory() as output:
            file_repository = FileRepository.mutable_one_per_file(
                '{}/{{name}}.json'.format(output),
                Serializer.json(),
                Vars.key('name')
            )
            file_repository.save(self.sample_content)
            result = filecmp.dircmp(output, original)
            self.assertFalse(result.diff_files)

    def test_write_sample_yaml(self):
        original = path.join(path.dirname(__file__), 'multiple/by-name/')
        with tempfile.TemporaryDirectory() as output:
            file_repository = FileRepository.mutable_one_per_file(
                '{}/{{name}}.yml'.format(output),
                Serializer.yaml(),
                Vars.key('name')
            )
            file_repository.save(self.sample_content)
            result = filecmp.dircmp(output, original)
            self.assertFalse(result.diff_files)

    def test_write_sample_toml(self):
        original = path.join(path.dirname(__file__), 'multiple/by-name/')
        with tempfile.TemporaryDirectory() as output:
            file_repository = FileRepository.mutable_one_per_file(
                '{}/{{name}}.toml'.format(output),
                Serializer.toml(),
                Vars.key('name')
            )
            file_repository.save(self.sample_content)
            result = filecmp.dircmp(output, original)
            self.assertFalse(result.diff_files)
