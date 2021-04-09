import tempfile
import os
from unittest import TestCase
from faker import Faker
from git import Repo

from test_git import provide_repo
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
            repository.save([{'name': 'settings123'}])

    @provide_repo(bare=False)
    def test_add_and_commit_strategy(self, repo):
        commit_message = fake.sentence()
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
        storage = GitStorage.from_repo(repo, session_strategy=SessionStrategy.AddAndCommit)
        with storage.open_session(commit_message) as session:
            repository = session.mutable_repository_for(settings_entity)
            repository.save([{'name': 'settings'}])
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
        self.assertEqual(repo.commit().message, commit_message)

    @provide_repo(bare=False)
    def test_add_and_commit_strategy_with_custom(self, repo):
        commit_message = fake.sentence()
        author = fake.name(), fake.email()
        committer = fake.name(), fake.email()
        settings_entity = Entity.from_raw({
            'name': 'settings',
            'singleton': True,
        })
        storage = GitStorage.from_repo(repo, session_strategy=SessionStrategy.AddAndCommit.create(author=author,
                                                                                                  committer=committer))
        with storage.open_session(commit_message) as session:
            repository = session.mutable_repository_for(settings_entity)
            repository.save([{'name': 'settings'}])
        commit = repo.commit()
        self.assertEqual(commit.message, commit_message)
        self.assertEqual(commit.author.name, author[0])
        self.assertEqual(commit.author.email, author[1])
        self.assertEqual(commit.committer.name, committer[0])
        self.assertEqual(commit.committer.email, committer[1])

    @provide_repo(name='local', bare=False)
    @provide_repo(name='remote', bare=True)
    def test_add_commit_and_push_strategy(self, local: Repo, remote: Repo):
        commit_message = fake.sentence()
        settings_entity = Entity.from_raw({
            'name': 'settings',
            'singleton': True,
        })
        local.create_remote('origin', url=remote.working_dir)
        storage = GitStorage.from_repo(local, session_strategy=SessionStrategy.AddCommitAndPush)
        with storage.open_session(commit_message) as session:
            repository = session.mutable_repository_for(settings_entity)
            repository.save([{
                'name': 'settings',
                'campaign': {
                    'name': fake.name(),
                }
            }])
        self.assertEqual(remote.commit().message, commit_message)

    @provide_repo(name='local', bare=False)
    @provide_repo(name='remote', bare=True, initial_commit=True)
    def test_pull_add_commit_and_push_strategy(self, local: Repo, remote: Repo):
        commit_message = fake.sentence()
        settings_entity = Entity.from_raw({
            'name': 'settings',
            'singleton': True,
        })
        local.create_remote('origin', url=remote.working_dir)
        storage = GitStorage.from_repo(local, session_strategy=SessionStrategy.PullAddCommitAndPush)
        with storage.open_session(commit_message) as session:
            repository = session.mutable_repository_for(settings_entity)
            repository.save([{
                'name': 'settings',
                'campaign': {
                    'name': fake.name(),
                }
            }])
        self.assertEqual(remote.commit().message, commit_message)
