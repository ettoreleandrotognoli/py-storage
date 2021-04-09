import tempfile
import functools
from git import Repo


class TemporaryRepository:

    def __init__(self, bare=True, initial_commit=False):
        self.bare = bare
        self.path = None
        self.initial_commit = initial_commit
        self.temporary_directory = tempfile.TemporaryDirectory()

    def __enter__(self):
        self.path = self.temporary_directory.__enter__()
        repo = Repo.init(self.path, bare=self.bare)
        if self.initial_commit:
            repo.index.commit("initial commit")
        return repo

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temporary_directory.__exit__(exc_type, exc_val, exc_tb)


def provide_repo(*args, name=None, **kwargs):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *_args, **_kwargs):
            with TemporaryRepository(*args, **kwargs) as repo:
                if name is None:
                    return fn(self, repo, *_args, **_kwargs)
                else:
                    return fn(self, *_args, **{name: repo}, **_kwargs)

        return wrapper

    return decorator
