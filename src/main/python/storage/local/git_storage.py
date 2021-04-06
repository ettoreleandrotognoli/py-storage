from __future__ import annotations

import abc
import logging
import tempfile
from logging import Logger

from git import Repo

from storage import MutableStorageSession, E, MutableRepository, Repository, Entity
from storage.api import SessionSupportStorage
from storage.local.file_repository import FileRepositoryListener, FileRepositoryFactory, FileRepository

__logger__: Logger = logging.getLogger(__name__)


class SessionFactory(abc.ABC):

    @abc.abstractmethod
    def __call__(self, origin: GitStorage, message: str) -> MutableStorageSession:
        raise NotImplementedError()


class SessionStrategy:
    class BaseSessionStrategy(MutableStorageSession, FileRepositoryListener):

        def __init__(self, storage: GitStorage, message: str):
            self.storage = storage
            self.message = message

        def repository_for(self, item_type: Entity[E]) -> Repository[E]:
            return self.storage.repository_for(item_type)

        def mutable_repository_for(self, item_type: Entity[E]) -> MutableRepository[E]:
            repository = self.storage.mutable_repository_for(item_type)
            repository.add_listener(self)
            return repository

        def __enter__(self):
            self.on_begin()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                self.on_error()
                raise exc_val
            self.on_success()

        def on_error(self):
            pass

        def on_success(self):
            pass

        def on_begin(self):
            pass

        def on_rewrite(self, file_name):
            pass

    class AddAndCommit(BaseSessionStrategy):

        def on_rewrite(self, file_name):
            self.storage.repo.index.add(file_name)

        def on_error(self):
            self.storage.repo.index.reset()
            self.storage.repo.git.clean('.', force=True)

        def on_success(self):
            self.storage.repo.index.commit(self.message)

    class PullAddAndCommit(AddAndCommit):

        def on_begin(self):
            self.storage.repo.git.pull(rebase=True)

    class PullAddCommitAndPush(PullAddAndCommit):

        def on_success(self):
            super().on_success()
            self.storage.repo.git.push()


class GitStorage(SessionSupportStorage):
    logger = __logger__

    def __init__(self, base_path: str, session_strategy=SessionStrategy.AddAndCommit):
        self.base_path = base_path
        self.repo = Repo(self.base_path)
        self.repository_factory = FileRepositoryFactory(self.base_path)
        self.session_strategy = session_strategy

    def open_session(self, message: str = None) -> MutableStorageSession:
        return self.session_strategy(self, message)

    def mutable_repository_for(self, item_type: Entity[E]) -> FileRepository[E]:
        repository = self.repository_factory.create(item_type)
        return repository

    def repository_for(self, item_type: Entity[E]) -> Repository[E]:
        return self.mutable_repository_for(item_type)

    @classmethod
    def create_from_url(cls, git_url: str, target: str = None, **kwargs):
        target = target or tempfile.TemporaryDirectory().name
        Repo.clone_from(git_url, target)
        return cls(target, **kwargs)

    @classmethod
    def empty(cls, target: str = None, **kwargs):
        target = target or tempfile.TemporaryDirectory().name
        Repo.init(target)
        return cls(target, **kwargs)
