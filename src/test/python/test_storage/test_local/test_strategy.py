from unittest import TestCase

from storage.local.file_repository import SingleFileStrategy, MultipleFileStrategy
from storage.predicate import Vars


class TestSingleFileStrategy(TestCase):

    def test_file_name(self):
        file_name = 'static.yml'
        strategy = SingleFileStrategy(file_name=file_name)
        self.assertEqual(strategy.file_for(None), file_name)

    def test_file_stream(self):
        file_name = 'static.yml'
        strategy = SingleFileStrategy(file_name=file_name)
        self.assertEqual(strategy.file_stream(), [file_name])

    def test_group_by(self):
        file_name = 'static.yml'
        strategy = SingleFileStrategy(file_name=file_name)
        self.assertEqual(strategy.group_by_file([]), {file_name: []})


class TestMultipleFileStrategy(TestCase):

    def test_file_name(self):
        item = {
            'name': 'bar',
            'parent': 'fuu',
        }
        template = '{parent}/file.yml'
        strategy = MultipleFileStrategy(
            template,
            {'parent': Vars.key('parent')}
        )
        self.assertEqual(strategy.file_for(item), template.format(parent=item['parent']))

    def test_glob_args(self):
        template = '{parent}/file.yml'
        strategy = MultipleFileStrategy(
            template,
            {'parent': Vars.key('parent')}
        )
        self.assertEqual(strategy.template_glob_args(), {'parent': '*'})

    def test_group_by(self):
        file_name = 'static.yml'
        strategy = SingleFileStrategy(file_name=file_name)
        self.assertEqual(strategy.group_by_file([]), {file_name: []})
