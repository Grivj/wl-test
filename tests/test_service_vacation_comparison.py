import unittest
from datetime import date
from uuid import UUID

from app.repository.employee import EmployeeRepository
from app.schema.vacation import VacationCreate
from app.service.vacation import VacationService
from app.service.vacation_comparison import VacationComparisonService
from tests.utils import get_test_db


class TestVacationComparisonService(unittest.TestCase):
    def setUp(self):
        self.session = get_test_db()
        self.service = VacationService
        self.comparison_service = VacationComparisonService

        self.jerome = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000000"),
                "first_name": "Jerome",
                "last_name": "Powell",
            },
        )
        self.jim = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000001"),
                "first_name": "Jim",
                "last_name": "Cramer",
            },
        )

    def test_employees_vacation_shared_days(self):
        # create some vacations
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=self.jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 4),
            ),
        )
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=self.jim.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 5),
            ),
        )
        self.service.create(
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
        print(shared_days)
        self.assertEqual(len(shared_days), 2)
        self.assertEqual(shared_days[0], date(2021, 1, 3))
        self.assertEqual(shared_days[1], date(2021, 1, 4))
