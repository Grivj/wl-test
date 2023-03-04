import unittest
from unittest.mock import MagicMock

from app.model import EmployeeModel
from app.repository.employee import EmployeeRepository


class TestEmployeeRepository(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repository = EmployeeRepository

    def test_get_by_id(self):
        self.session.query().filter().one_or_none.return_value = EmployeeModel()
        self.assertIsNotNone(self.repository.get_by_id(self.session, 1))

    def test_get_by_id_not_found(self):
        self.session.query().filter().one_or_none.return_value = None
        self.assertIsNone(self.repository.get_by_id(self.session, 1))
