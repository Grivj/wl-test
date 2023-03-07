import unittest
from datetime import date

from app.api.dependencies import (
    get_employee_repository,
    get_vacation_comparison_service,
    get_vacation_service,
)
from app.schema.employee import EmployeeCreate
from app.schema.vacation import VacationCreate
from tests.utils import get_test_db


class TestVacationComparisonService(unittest.TestCase):
    async def asyncSetUp(self):
        self.session = get_test_db()
        self.vacation_service = await get_vacation_service()
        self.comparison_service = await get_vacation_comparison_service()
        self.employee_repository = await get_employee_repository()

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

    async def test_employees_vacation_shared_days(self):
        # create some vacations
        self.vacation_service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 4),
            ),
        )
        self.vacation_service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jim.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 5),
            ),
        )
        self.vacation_service.create_vacation(
            self.session,
            VacationCreate(
                employee_id=self.jim.id,
                start_date=date(2021, 1, 7),
                end_date=date(2021, 1, 10),
            ),
        )

        # they share 2 days of vacation
        # 2021-01-03
        # 2021-01-04

        shared_days = self.comparison_service.compare_employees_vacations(
            self.session, self.jerome, self.jim, date(2021, 1, 1), date(2021, 1, 20)
        )
        self.assertEqual(len(shared_days), 2)
        self.assertEqual(shared_days[0], date(2021, 1, 3))
        self.assertEqual(shared_days[1], date(2021, 1, 4))
