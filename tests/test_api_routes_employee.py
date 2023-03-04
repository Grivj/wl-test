import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.api.routes.employee import create_employee, get_employee
from app.repository.employee import EmployeeRepository
from app.schema.employee import Employee, EmployeeCreate


class TestEmployeeIsolatedRoute(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repository = EmployeeRepository

    @patch.object(
        EmployeeRepository,
        "get",
        return_value=Employee(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            first_name="John",
            last_name="Doe",
        ),
    )
    def test_get_employee(self, get: MagicMock):
        response = get_employee(
            self.session, employee_id=UUID("00000000-0000-0000-0000-000000000001")
        )
        assert response == Employee(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            first_name="John",
            last_name="Doe",
        )

    @patch.object(
        EmployeeRepository,
        "create",
        return_value=Employee(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            first_name="John",
            last_name="Doe",
        ),
    )
    def test_create_employee(self, create: MagicMock):
        employee = EmployeeCreate(first_name="John", last_name="Doe")
        response = create_employee(session=self.session, employee=employee)
        assert response == Employee(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            first_name="John",
            last_name="Doe",
        )
        create.assert_called_once_with(session=self.session, obj_in=employee.dict())
