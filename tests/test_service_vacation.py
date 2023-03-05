import unittest
from datetime import date
from uuid import UUID

from app.model import VacationModel
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate, VacationType
from app.service.vacation import VacationService
from tests.utils import get_test_db


class TestVacationService(unittest.TestCase):
    def setUp(self):
        self.session = get_test_db()
        self.service = VacationService

    def test_create_vacation(self):
        vacation_data = VacationCreate(
            employee_id=UUID("00000000-0000-0000-0000-000000000000"),
            start_date=date(2021, 1, 1),
            end_date=date(2021, 1, 5),
            type=VacationType.PAID,
        )

        vacation = self.service.create(self.session, vacation_data)

        self.assertIsInstance(vacation, VacationModel)
        self.assertEqual(
            vacation.employee_id, UUID("00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(vacation.start_date, date(2021, 1, 1))
        self.assertEqual(vacation.end_date, date(2021, 1, 5))
        self.assertEqual(vacation.type, VacationType.PAID)

    def test_create_vacation_with_overlapping_vacations(self):
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ).dict(),
        )
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ).dict(),
        )
        vacation_data = VacationCreate(
            employee_id=UUID("00000000-0000-0000-0000-000000000000"),
            start_date=date(2021, 1, 2),
            end_date=date(2021, 1, 6),
            type=VacationType.PAID,
        )

        vacation = self.service.create(self.session, vacation_data)

        self.assertIsInstance(vacation, VacationModel)
        self.assertEqual(
            vacation.employee_id, UUID("00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(vacation.start_date, date(2021, 1, 1))
        self.assertEqual(vacation.end_date, date(2021, 1, 7))
        self.assertEqual(vacation.type, VacationType.PAID)

    def test_create_vacation_with_contiguous_vacations(self):
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ).dict(),
        )
        vacation_data = VacationCreate(
            employee_id=UUID("00000000-0000-0000-0000-000000000000"),
            start_date=date(2021, 1, 6),
            end_date=date(2021, 1, 10),
            type=VacationType.PAID,
        )

        vacation = self.service.create(self.session, vacation_data)

        self.assertIsInstance(vacation, VacationModel)
        self.assertEqual(
            vacation.employee_id, UUID("00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(vacation.start_date, date(2021, 1, 1))
        self.assertEqual(vacation.end_date, date(2021, 1, 10))
        self.assertEqual(vacation.type, VacationType.PAID)

    def test_create_vacation_with_overlapping_vacations_but_wrong_type(self):
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ).dict(),
        )
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ).dict(),
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

    def test_update_vacation(self):
        # create a vacation
        vacation = self.service.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
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
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 2),
                end_date=date(2021, 1, 6),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(updated_vacation, VacationModel)

        # assert the updates were successful
        self.assertEqual(
            updated_vacation.employee_id, UUID("00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(updated_vacation.start_date, date(2021, 1, 2))
        self.assertEqual(updated_vacation.end_date, date(2021, 1, 6))
        self.assertEqual(updated_vacation.type, VacationType.PAID)

    def test_update_vacation_with_overlapping_vacations(self):
        # create a vacation
        vacation = self.service.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(vacation, VacationModel)

        # create another vacation
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ).dict(),
        )

        # update the vacation
        updated_vacation = self.service.update(
            self.session,
            vacation,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 2),
                end_date=date(2021, 1, 6),
                type=VacationType.PAID,
            ),
        )
        self.assertIsInstance(updated_vacation, VacationModel)

        # assert the updates were successful
        self.assertEqual(
            updated_vacation.employee_id, UUID("00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(updated_vacation.start_date, date(2021, 1, 2))
        self.assertEqual(updated_vacation.end_date, date(2021, 1, 7))
        self.assertEqual(updated_vacation.type, VacationType.PAID)

    def test_get_employees_in_vacation(self):
        # create some employees
        jerome = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000000"),
                "first_name": "Jerome",
                "last_name": "Powell",
            },
        )
        jim = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000001"),
                "first_name": "Jim",
                "last_name": "Cramer",
            },
        )
        elisabeth = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000002"),
                "first_name": "Elisabeth",
                "last_name": "Warren",
            },
        )

        # create some vacations
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 3),
                type=VacationType.PAID,
            ),
        )
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=jerome.id,
                start_date=date(2021, 1, 5),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=jim.id,
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 4),
                type=VacationType.UNPAID,
            ),
        )
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=elisabeth.id,
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
        self.assertEqual(employees, {jerome, jim})

    def test_get_employees_in_vacation_by_type(self):
        # create some employees
        jerome = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000000"),
                "first_name": "Jerome",
                "last_name": "Powell",
            },
        )
        jim = EmployeeRepository.create(
            self.session,
            {
                "id": UUID("00000000-0000-0000-0000-000000000001"),
                "first_name": "Jim",
                "last_name": "Cramer",
            },
        )

        # create some vacations
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=jerome.id,
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 3),
                type=VacationType.PAID,
            ),
        )
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=jerome.id,
                start_date=date(2021, 1, 5),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ),
        )
        self.service.create(
            self.session,
            VacationCreate(
                employee_id=jim.id,
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
        self.assertEqual(employees, {jim})
