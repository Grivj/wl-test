import unittest
from datetime import date
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.model import VacationModel
from app.model.base import BaseModel
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate, VacationType


def get_test_db() -> scoped_session:
    engine = create_engine("sqlite:///:memory:")
    session = sessionmaker(bind=engine)
    scoped = scoped_session(session)
    BaseModel.metadata.create_all(engine)  # type: ignore
    return scoped


class TestVacationRepository(unittest.TestCase):
    def setUp(self):
        self.session = get_test_db()
        self.repository = VacationModel

    def tearDown(self):
        BaseModel.metadata.drop_all(self.session.bind)  # type: ignore

    def test_get_overlapping_vacations(self):
        vacation_1 = VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ).dict(),
        )
        vacation_2 = VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ).dict(),
        )
        # the vacations overlap on 2021-01-03 to 2021-01-05
        overlapping_vacations = VacationRepository.get_overlapping_vacations(
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

    def test_get_overlapping_vacations_with_no_overlap(self):
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
                start_date=date(2021, 1, 6),
                end_date=date(2021, 1, 7),
                type=VacationType.PAID,
            ).dict(),
        )
        overlapping_vacations = VacationRepository.get_overlapping_vacations(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 2, 3),
                end_date=date(2021, 2, 7),
                type=VacationType.PAID,
            ),
        )
        self.assertEqual(len(overlapping_vacations), 0)

    def test_get_overlapping_vacations_only_same_type(self):
        VacationRepository.create(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 5),
                type=VacationType.PAID,
            ).dict(),
        )
        overlapping_vacations = VacationRepository.get_overlapping_vacations(
            self.session,
            VacationCreate(
                employee_id=UUID("00000000-0000-0000-0000-000000000000"),
                start_date=date(2021, 1, 3),
                end_date=date(2021, 1, 7),
                type=VacationType.UNPAID,
            ),
        )
        self.assertEqual(len(overlapping_vacations), 0)
