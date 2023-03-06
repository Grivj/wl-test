import unittest

from pydantic import ValidationError

from app.repository.employee import EmployeeRepository
from app.schema.employee import EmployeeCreate
from tests.utils import get_test_db


class TestEmployeeRepository(unittest.TestCase):
    def setUp(self):
        self.session = get_test_db()
        self.repository = EmployeeRepository

        self.dummy_employee = EmployeeCreate(
            first_name="Jerome",
            last_name="Powell",
        )

    def test_create_employee(self):
        # test successful creation
        employee = self.repository.create_employee(self.session, self.dummy_employee)
        self.assertEqual(employee.first_name, self.dummy_employee.first_name)

        # test invalid input (should raise ValidationError)
        with self.assertRaises(ValidationError):
            self.repository.create_employee(self.session, EmployeeCreate())  # type: ignore

        # test get employee by id
        employee = self.repository.get_employee_by_id(self.session, employee.id)
        self.assertIsNotNone(employee)
        assert employee is not None
        self.assertEqual(employee.first_name, self.dummy_employee.first_name)

    def test_delete_employee(self):
        # test delete employee
        employee = self.repository.create_employee(self.session, self.dummy_employee)
        self.repository.delete_employee(self.session, employee)
        employee = self.repository.get_employee_by_id(self.session, employee.id)
        self.assertIsNone(employee)
