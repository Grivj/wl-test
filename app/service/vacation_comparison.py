from dataclasses import dataclass
from datetime import date, timedelta
from typing import Generator

from sqlalchemy.orm import Session

from app.model import EmployeeModel, VacationModel
from app.repository.vacation import VacationRepository


def get_date_range(start_date: date, end_date: date) -> Generator[date, None, None]:
    """Returns a list of dates between the given start and end date."""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


@dataclass
class _VacationComparisonService:
    repository = VacationRepository

    def compare_employees_vacations(
        self,
        session: Session,
        employee_1: EmployeeModel,
        employee_2: EmployeeModel,
        start_date: date,
        end_date: date,
    ) -> list[date]:
        employee_1_vacations = self.repository.get_employee_vacations(
            session, employee_1, start_date, end_date
        )
        employee_2_vacations = self.repository.get_employee_vacations(
            session, employee_2, start_date, end_date
        )
        return self.compare_vacations(employee_1_vacations, employee_2_vacations)

    def compare_vacations(
        self, vacations_1: list[VacationModel], vacations_2: list[VacationModel]
    ) -> list[date]:
        """Returns a list of dates that are in both vacation lists."""
        dates_1 = self._get_vacation_dates(vacations_1)
        dates_2 = self._get_vacation_dates(vacations_2)
        return sorted(list(dates_1 & dates_2))

    def _get_vacation_dates(self, vacations: list[VacationModel]) -> set[date]:
        """Returns a set of dates for the given vacations."""
        return {
            date
            for vacation in vacations
            for date in get_date_range(vacation.start_date, vacation.end_date)
        }


VacationComparisonService = _VacationComparisonService()
