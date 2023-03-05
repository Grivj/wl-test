import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.api.routes.employee import create_employee
from app.repository.employee import EmployeeRepository
from app.schema.employee import Employee, EmployeeCreate

DUMMY_EMPLOYEE = Employee(
    id=UUID("00000000-0000-0000-0000-000000000001"),
    first_name="John",
    last_name="Doe",
)


class TestEmployeeIsolatedRoute(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repository = EmployeeRepository

    @patch.object(EmployeeRepository, "create", return_value=DUMMY_EMPLOYEE)
    def test_create_employee(self, create: MagicMock):
        employee = EmployeeCreate(first_name="John", last_name="Doe")
        response = create_employee(session=self.session, employee=employee)
        create.assert_called_once_with(session=self.session, obj_in=employee.dict())
        assert response == DUMMY_EMPLOYEE
