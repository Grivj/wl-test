import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.api.routes.employee import create_employee
from app.repository.employee import EmployeeRepository
from app.schema.employee import Employee, EmployeeCreate
from app.service.employee import EmployeeService

DUMMY_EMPLOYEE = Employee(
    id=UUID("00000000-0000-0000-0000-000000000001"),
    first_name="John",
    last_name="Doe",
    timezone="Europe/Paris",
    team_id=None,
)


class TestEmployeeIsolatedRoute(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repository = EmployeeRepository

    @patch.object(EmployeeService, "create_with_balance", return_value=DUMMY_EMPLOYEE)
    def test_create_employee(self, create: MagicMock):
        employee = EmployeeCreate(
            first_name=DUMMY_EMPLOYEE.first_name, last_name=DUMMY_EMPLOYEE.last_name
        )
        response = create_employee(session=self.session, employee=employee)
        assert response == DUMMY_EMPLOYEE
