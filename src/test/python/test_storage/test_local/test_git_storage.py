import tempfile
import os
from unittest import TestCase
from faker import Faker

from storage import Entity
from storage.local.git_storage import GitStorage, SessionStrategy

fake = Faker()


class TestGitStorage(TestCase):

    def test_clone(self):
        git_url = 'https://github.com/ettoreleandrotognoli/py-storage.git'
        with tempfile.TemporaryDirectory() as tmp:
            storage = GitStorage.create_from_url(git_url, tmp)

    def test_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            GitStorage.empty(tmp)
            self.assertTrue(os.path.exists(os.path.join(tmp, '.git')))

    def test_singleton_entity(self):
        entity = Entity.from_raw({
            'name': 'settings',
            'singleton': True,
        })
        with tempfile.TemporaryDirectory() as tmp:
            storage = GitStorage.empty(tmp)
            repository = storage.mutable_repository_for(entity)
            repository.save([{'name': 'settings'}])
            print(list(repository.stream()))
            repository.save([{'name': 'settings123'}])
            print(list(repository.stream()))

    def test_full_entity(self):
        settings_entity = Entity.from_raw({
            'name': 'settings',
            'singleton': True,
        })
        user_entity = Entity.from_raw({
            'name': 'user',
            'pk': 'name',
        })
        character_entity = Entity.from_raw({
            'name': 'character',
            'pk': 'name',
            'parent': {
                'name': 'user',
                'parent_id': 'owner'
            }
        })
        with tempfile.TemporaryDirectory() as tmp:
            storage = GitStorage.empty(tmp)
            repository = storage.mutable_repository_for(settings_entity)
            repository.save([{'name': 'settings'}])
            repository = storage.mutable_repository_for(user_entity)
            repository.save([
                {'name': 'fuu'},
                {'name': 'bar'},
            ])
            repository = storage.mutable_repository_for(character_entity)
            repository.save([
                {'owner': 'fuu', 'name': fake.name()},
                {'owner': 'fuu', 'name': fake.name()},
                {'owner': 'bar', 'name': fake.name()},
                {'owner': 'bar', 'name': fake.name()},
            ])
            print(storage)

    def test_full_entity_with_session(self):
        settings_entity = Entity.from_raw({
            'name': 'settings',
            'singleton': True,
        })
        user_entity = Entity.from_raw({
            'name': 'user',
            'pk': 'name',
        })
        character_entity = Entity.from_raw({
            'name': 'character',
            'pk': 'name',
            'parent': {
                'name': 'user',
                'parent_id': 'owner'
            }
        })
        with tempfile.TemporaryDirectory() as tmp:
            storage = GitStorage.create_from_url(
                'git@github.com:ettoreleandrotognoli/test.git', tmp,
                session_strategy=SessionStrategy.PullAddCommitAndPush
            )
            with storage.open_session('another test') as session:
                repository = session.mutable_repository_for(settings_entity)
                repository.save([{
                    'name': 'settings',
                    'campaign': {
                        'name': 'Moonlight Sonata',
                    }
                }])
                repository = session.mutable_repository_for(user_entity)
                repository.save([
                    {'name': 'fuu'},
                    {'name': 'bar'},
                ])
                repository = session.mutable_repository_for(character_entity)
                repository.save([
                    {'owner': 'fuu', 'name': fake.name()},
                    {'owner': 'fuu', 'name': fake.name()},
                    {'owner': 'bar', 'name': fake.name()},
                    {'owner': 'bar', 'name': fake.name()},
                ])
