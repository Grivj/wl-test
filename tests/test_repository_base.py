import unittest
import uuid as uid
from unittest.mock import MagicMock

from app.model.base import BaseModel
from app.repository.base import BaseRepository, add_and_commit


class TestBaseRepository(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repository = BaseRepository[BaseModel](model=BaseModel)

    def test_add_and_commit_success(self):
        obj = MagicMock()
        result = add_and_commit(self.session, obj)
        self.assertEqual(result, obj)

    def test_get_by_id(self):
        self.session.query().filter().one_or_none.return_value = BaseModel()  # type: ignore
        self.assertIsNotNone(self.repository.get_by_id(self.session, id=uid.uuid4()))

    def test_get_by_id_not_found(self):
        self.session.query().filter().one_or_none.return_value = None  # type: ignore
        self.assertIsNone(self.repository.get_by_id(self.session, id=uid.uuid4()))
