import unittest
from datetime import date
from uuid import UUID

from app.model import VacationModel
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate, VacationType
from app.service.vacation import VacationService
from app.service.vacation_validators import (
    OverlappingVacationTypeValidator,
    VacationValidator,
)
from tests.utils import get_test_db


class TestVacationService(unittest.TestCase):
    def setUp(self):
        self.session = get_test_db()
        self.validators: list[VacationValidator] = [OverlappingVacationTypeValidator]
        self.service = VacationService(self.validators)

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
