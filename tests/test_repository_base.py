import unittest
from unittest.mock import MagicMock

from app.repository.base import add_and_commit


class TestBaseRepository(unittest.TestCase):
    def test_add_and_commit_success(self):
        session = MagicMock()
        obj = MagicMock()
        result = add_and_commit(session, obj)
        self.assertEqual(result, obj)
