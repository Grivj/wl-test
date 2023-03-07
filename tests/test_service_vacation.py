import unittest
from datetime import date
from uuid import UUID

from app.api.dependencies import get_employee_repository, get_vacation_service
from app.model import VacationModel
from app.schema.employee import EmployeeCreate
from app.schema.vacation import VacationCreate, VacationType
from tests.utils import get_test_db


class TestVacationService(unittest.TestCase):
    async def asyncSetUp(self):
        self.session = get_test_db()
        self.service = await get_vacation_service()
        self.employee_repository = await get_employee_repository()

        # create some dummy employees
        self.jerome = self.employee_repository.create_employee(
            self.session,
            EmployeeCreate(
                first_name="Jerome",
                last_name="Powell",
            ),
        )
        self.jim = self.employee_repository.create_employee(
            self.session,
            EmployeeCreate(
                first_name="Jim",
                last_name="Cramer",
            ),
        )
        self.elisabeth = self.employee_repository.create_employee(
            self.session,
            EmployeeCreate(
                first_name="Elisabeth",
                last_name="Warren",
            ),
        )

    async def test_create_vacation(self):
        vacation_data = VacationCreate(
            employee_id=self.jerome.id,
            start_date=date(2021, 1, 1),
            end_date=date(2021, 1, 5),
            type=VacationType.PAID,
        )

        vacation = self.service.create_vacation(self.session, vacation_data)

        self.assertIsInstance(vacation, VacationModel)
        self.assertEqual(vacation.employee_id, self.jerome.id)
        self.assertEqual(vacation.start_date, date(2021, 1, 1))
        self.assertEqual(vacation.end_date, date(2021, 1, 5))
        self.assertEqual(vacation.type, VacationType.PAID)

    async def test_create_vacation_with_overlapping_vacations(self):
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        vacation_data = VacationCreate(
            employee_id=self.jerome.id,
            start_date=date(2021, 1, 2),
            end_date=date(2021, 1, 6),
            type=VacationType.PAID,
        )

        vacation = self.service.create_vacation(self.session, vacation_data)

        self.assertIsInstance(vacation, VacationModel)
        self.assertEqual(vacation.employee_id, self.jerome.id)
        self.assertEqual(vacation.start_date, date(2021, 1, 1))
        self.assertEqual(vacation.end_date, date(2021, 1, 7))
        self.assertEqual(vacation.type, VacationType.PAID)

    async def test_create_vacation_with_contiguous_vacations(self):
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        vacation_data = VacationCreate(
            employee_id=self.jerome.id,
            start_date=date(2021, 1, 6),
            end_date=date(2021, 1, 10),
            type=VacationType.PAID,
        )

        vacation = self.service.create_vacation(self.session, vacation_data)

        self.assertIsInstance(vacation, VacationModel)
        self.assertEqual(vacation.employee_id, self.jerome.id)
        self.assertEqual(vacation.start_date, date(2021, 1, 1))
        self.assertEqual(vacation.end_date, date(2021, 1, 10))
        self.assertEqual(vacation.type, VacationType.PAID)

    async def test_create_vacation_with_overlapping_vacations_but_wrong_type(self):
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        # this vacation overlaps with the previous two
        # but it's of a different type
        vacation_data = VacationCreate(
            employee_id=UUID("00000000-0000-0000-0000-000000000000"),
            start_date=date(2021, 1, 2),
            end_date=date(2021, 1, 6),
            type=VacationType.UNPAID,
        )

        with self.assertRaises(ValueError):
            self.service.create(self.session, vacation_data)

    async def test_update_vacation(self):
        # create a vacation
        vacation = self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(vacation, VacationModel)

        # update the vacation
        updated_vacation = self.service.update(
            self.session,
            vacation,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 2),
                end_date=date(2021, 1, 6),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(updated_vacation, VacationModel)

        # assert the updates were successful
        self.assertEqual(updated_vacation.employee_id, self.jerome.id)
        self.assertEqual(updated_vacation.start_date, date(2021, 1, 2))
        self.assertEqual(updated_vacation.end_date, date(2021, 1, 6))
        self.assertEqual(updated_vacation.type, VacationType.PAID)

    async def test_update_vacation_with_overlapping_vacations(self):
        # create a vacation
        vacation = self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(vacation, VacationModel)

        # create another vacation
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )

        # update the vacation
        updated_vacation = self.service.update(
            self.session,
            vacation,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 2),
                end_date=date(2021, 1, 6),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(updated_vacation, VacationModel)

        # assert the updates were successful
        self.assertEqual(updated_vacation.employee_id, self.jerome.id)
        self.assertEqual(updated_vacation.start_date, date(2021, 1, 2))
        self.assertEqual(updated_vacation.end_date, date(2021, 1, 7))
        self.assertEqual(updated_vacation.type, VacationType.PAID)

    async def test_get_employees_in_vacation(self):
        # create some vacations
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 3),
                type=VacationType.PAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 5),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jim.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 4),
                type=VacationType.UNPAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.elisabeth.id,
                start_date=date(2021, 1, 11),
                end_date=date(2021, 1, 20),
                type=VacationType.PAID,
            ),
        )

        # get the employees in vacation
        # elisabeth is not in vacation in this period
        employees = self.service.get_employees_in_vacation(
            self.session, date(2021, 1, 1), date(2021, 1, 10)
        )

        # assert the employees were returned
        self.assertIsInstance(employees, set)
        self.assertEqual(len(employees), 2)
        self.assertEqual(employees, {self.jerome, self.jim})

    async def test_get_employees_in_vacation_by_type(self):
        # create some vacations
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 3),
                type=VacationType.PAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 5),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        self.service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jim.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 4),
                type=VacationType.UNPAID,
            ),
        )

        # get the employees in paid vacation
        employees = self.service.get_employees_in_vacation(
            self.session, date(2021, 1, 1), date(2021, 1, 10), VacationType.UNPAID
        )

        # assert the employees were returned
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees, {self.jim})
