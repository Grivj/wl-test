import unittest

from pydantic import ValidationError

from app.api.dependencies import get_employee_repository
from app.schema.employee import EmployeeCreate, EmployeeUpdate
from tests.utils import get_test_db


class TestEmployeeRepository(unittest.TestCase):
    async def asyncSetUp(self):
        self.session = get_test_db()
        self.repository = await get_employee_repository()

        self.dummy_employee = EmployeeCreate(
            first_name="Jerome",
            last_name="Powell",
        )

    async def test_create_employee(self):
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

    async def test_delete_employee(self):
        # test delete employee
        employee = self.repository.create_employee(self.session, self.dummy_employee)
        self.repository.delete_employee(self.session, employee)
        employee = self.repository.get_employee_by_id(self.session, employee.id)
        self.assertIsNone(employee)

    async def test_update_employee(self):
        # create employee
        employee = self.repository.create_employee(self.session, self.dummy_employee)

        # update employee
        updated_employee_data = EmployeeUpdate(first_name="Janet")
        updated_employee = self.repository.update_employee(
            self.session, employee, updated_employee_data
        )
        # at that point, the employee has been updated in the database and
        # should be named Janet Powell

        # retrieve updated employee
        retrieved_employee = self.repository.get_employee_by_id(
            self.session, employee.id
        )

        self.assertIsNotNone(retrieved_employee)
        assert retrieved_employee is not None

        # check that employee was successfully updated
        self.assertEqual(updated_employee.first_name, "Janet")
        self.assertEqual(retrieved_employee.first_name, "Janet")
        self.assertEqual(updated_employee.id, retrieved_employee.id)
