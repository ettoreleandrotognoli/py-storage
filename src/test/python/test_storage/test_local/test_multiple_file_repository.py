import filecmp
import tempfile
from os import path
from unittest import TestCase

from storage.local.file_repository import FileRepository
from storage.predicate import Vars, Const
from storage.serializer import Serializer


class TestReadOnePerFileRepository(TestCase):
    sample_content = [
        {"version": 2, "language": "python"},
        {"version": 3, "language": "python"},
        {"version": 8, "language": "java"},
        {"version": 11, "language": "java"},
    ]

    def test_read_sample_yml(self):
        file_repository = FileRepository.multiple_file(
            path.join(path.dirname(__file__), 'multiple/by-parent/{language}.yml'),
            Serializer.yaml()
        )
        read_sample = sorted(list(file_repository.stream()), key=Vars.key("version"))
        self.assertListEqual(read_sample, self.sample_content)

    def test_read_sample_json(self):
        file_repository = FileRepository.multiple_file(
            path.join(path.dirname(__file__), 'multiple/by-parent/{language}.json'),
            Serializer.json()
        )
        read_sample = sorted(list(file_repository.stream()), key=Vars.key("version"))
        self.assertListEqual(read_sample, self.sample_content)

    def test_read_sample_toml(self):
        file_repository = FileRepository.multiple_file(
            path.join(path.dirname(__file__), 'multiple/by-parent/{language}.toml'),
            Serializer.toml()
        )
        read_sample = sorted(list(file_repository.stream()), key=Vars.key("version"))
        self.assertListEqual(read_sample, self.sample_content)

    def test_write_sample_yml(self):
        original = path.join(path.dirname(__file__), 'multiple/by-parent/')
        with tempfile.TemporaryDirectory() as output:
            file_repository = FileRepository.mutable_multiple_file(
                '{}/{{language}}.yml'.format(output),
                Serializer.yaml(),
                Vars.key('language') + ':' + Vars.key('version').cast(str)
            )
            file_repository.save(self.sample_content)
            result = filecmp.dircmp(output, original, ignore=['.json', '.toml'])
            self.assertFalse(result.diff_files)

    def test_write_sample_json(self):
        original = path.join(path.dirname(__file__), 'multiple/by-parent/')
        with tempfile.TemporaryDirectory() as output:
            file_repository = FileRepository.mutable_multiple_file(
                '{}/{{language}}.json'.format(output),
                Serializer.json(),
                Vars.key('language') + ':' + Vars.key('version').cast(str)
            )
            file_repository.save(self.sample_content)
            result = filecmp.dircmp(output, original, ignore=['.yaml', '.toml'])
            self.assertFalse(result.diff_files)

    def test_write_sample_toml(self):
        original = path.join(path.dirname(__file__), 'multiple/by-parent/')
        with tempfile.TemporaryDirectory() as output:
            file_repository = FileRepository.mutable_multiple_file(
                '{}/{{language}}.toml'.format(output),
                Serializer.toml(),
                Vars.key('language') + ':' + Vars.key('version').cast(str)
            )
            file_repository.save(self.sample_content)
            result = filecmp.dircmp(output, original, ignore=['.yaml', '.json'])
            self.assertFalse(result.diff_files)
