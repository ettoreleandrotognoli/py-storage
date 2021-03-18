import tempfile
from faker import Faker
from unittest import TestCase
from git import Repo

fake = Faker()


class GitPythonExampleTest(TestCase):

    def test_init_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            commit_message = fake.sentence()
            repo = Repo.init(tmp)
            repo.index.commit(commit_message)
            self.assertEqual(repo.commit().message, commit_message)
