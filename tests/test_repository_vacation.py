import unittest
from datetime import date
from uuid import UUID

from fastapi import Depends

from app.api.dependencies import get_employee_repository, get_vacation_repository
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository
from app.schema.employee import EmployeeCreate
from app.schema.vacation import VacationCreate, VacationType
from tests.utils import get_test_db


class TestVacationRepository(unittest.TestCase):
    async def asyncSetUp(self):
        self.session = get_test_db()
        self.repository: VacationRepository = await get_vacation_repository()

    async def test_get_overlapping_vacations(self):
        vacation_1 = self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        vacation_2 = self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        # the vacations overlap on 2021-01-03 to 2021-01-05
        overlapping_vacations = self.repository.get_overlapping_vacations(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        self.assertEqual(len(overlapping_vacations), 2)

        # check that the overlapping vacations are the ones we expect
        self.assertEqual(overlapping_vacations[0].id, vacation_1.id)
        self.assertEqual(overlapping_vacations[1].id, vacation_2.id)

    async def test_get_overlapping_vacations_with_no_overlap(self):
        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 6),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        overlapping_vacations = self.repository.get_overlapping_vacations(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 2, 3),
                end_date=date(2021, 2, 7),
                type=VacationType.PAID,
            ),
        )
        self.assertEqual(len(overlapping_vacations), 0)

    async def test_get_overlapping_vacations_only_same_employee(self):
        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        overlapping_vacations = self.repository.get_overlapping_vacations(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000001"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        self.assertEqual(len(overlapping_vacations), 0)

    async def test_get_employee_vacations_time_constrained(
        self, employee_repository: EmployeeRepository = Depends(get_employee_repository)
    ):
        employee = employee_repository.create_employee(
            self.session,
            EmployeeCreate(
                first_name="Jerome",
                last_name="Powell",
            ),
        )

        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=employee.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
            ),
        )
        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=employee.id,
                start_date=date(2021, 1, 6),
                end_date=date(2021, 1, 7),
            ),
        )
        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=employee.id,
                start_date=date(2021, 2, 1),
                end_date=date(2021, 2, 5),
            ),
        )
        self.repository.create_vacation(
            self.session,
            VacationCreate(
                employee_id=employee.id,
                start_date=date(2021, 2, 6),
                end_date=date(2021, 2, 7),
            ),
        )
        # get vacations from 2021-01-01 to 2021-01-31
        vacations = self.repository.get_employee_vacations(
            self.session, employee, date(2021, 1, 1), date(2021, 1, 31)
        )
        self.assertEqual(len(vacations), 2)

        # get vacations from 2021-02-01 to 2021-02-28
        vacations = self.repository.get_employee_vacations(
            self.session, employee, date(2021, 2, 1), date(2021, 2, 28)
        )
        self.assertEqual(len(vacations), 2)
