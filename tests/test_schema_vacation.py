import unittest
from datetime import date
from uuid import UUID

from app.schema.vacation import VacationBase, VacationType


class TestVacationBaseSchema(unittest.TestCase):
    def test_raises_on_wrong_dates(self):
        # end_date < start_date
        with self.assertRaises(ValueError):
            VacationBase(
                start_date=date(2023, 1, 5),
                end_date=date(2023, 1, 1),
                employee_id=UUID("00000000-0000-0000-0000-000000000001"),
                type=VacationType.PAID,
            )

    def test_valid_dates(self):
        # end_date >= start_date
        self.assertEqual(
            VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 5),
                employee_id=UUID("00000000-0000-0000-0000-000000000001"),
                type=VacationType.PAID,
            ).end_date,
            date(2023, 1, 5),
        )
