from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.model import EmployeeModel, VacationModel
from app.repository.balance import BalanceRepository
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate, VacationType

from .vacation_validators import (
    OverlappingVacationTypeValidator,
    VacationValidator,
    get_calendar_for_tz,
)


@dataclass
class _VacationService:
    validators: list[VacationValidator]
    repository = VacationRepository
    balance_repository = BalanceRepository

    def create(self, session: Session, vacation: VacationCreate) -> VacationModel:
        overlapping_vacations = self.repository.get_overlapping_vacations(
            session, vacation
        )

        for validator in self.validators:
            validator.validate(
                session, vacation=vacation, overlapping_vacations=overlapping_vacations
            )
        if overlapping_vacations:
            return self.handle_overlapping_vacations(
                session, vacation, overlapping_vacations
            )
        created_vacation = self.repository.create(session, vacation.dict())
        # updating the employee balance
        print("created_vacation")
        self.update_balance_by_vacation(session, created_vacation)
        return created_vacation

    def update(
        self,
        session: Session,
        old_vacation: VacationModel,
        new_vacation: VacationCreate,
    ) -> VacationModel:
        overlapping_vacations = self.repository.get_overlapping_vacations(
            session, new_vacation
        )
        # remove the old vacation from the overlapping vacations
        overlapping_vacations = [
            v for v in overlapping_vacations if v.id != old_vacation.id
        ]

        for validator in self.validators:
            validator.validate(
                session,
                vacation=new_vacation,
                overlapping_vacations=overlapping_vacations,
            )
        if overlapping_vacations:
            return self.handle_overlapping_vacations(
                session, new_vacation, overlapping_vacations
            )
        updated_vacation = self.repository.update(
            session,
            VacationModel(employee=old_vacation.employee, **new_vacation.dict()),  # type: ignore
        )
        print("updated_vacation")
        # updating the employee balance
        self.update_balance_by_vacation(session, updated_vacation)
        return updated_vacation

    def handle_overlapping_vacations(
        self,
        session: Session,
        vacation: VacationCreate,
        overlapping_vacations: list[VacationModel],
    ) -> VacationModel:
        merged_vacation = self.merge_vacations(session, vacation, overlapping_vacations)
        self.repository.delete_many(session, overlapping_vacations)
        created_vacation = self.repository.create(session, merged_vacation.dict())
        # updating the employee balance
        self.update_balance_by_vacation(session, created_vacation)
        return created_vacation

    def update_balance_by_vacation(
        self,
        session: Session,
        vacation: VacationModel,
    ) -> None:
        # get the vacation cost in days
        vacation_cost = self.get_vacation_number_of_workdays(vacation)
        # update the employee balance
        print(vacation.employee, vacation_cost)
        self.balance_repository.update_balance(
            session, vacation.employee, vacation_cost
        )

    def merge_vacations(
        self,
        session: Session,
        vacation: VacationCreate,
        overlapping_vacations: list[VacationModel],
    ) -> VacationCreate:
        # merge the overlapping vacations into the new vacation
        start_date = min(v.start_date for v in overlapping_vacations)
        end_date = max(v.end_date for v in overlapping_vacations)
        vacation.start_date = min(vacation.start_date, start_date)
        vacation.end_date = max(vacation.end_date, end_date)
        return vacation

    def get_employees_in_vacation(
        self,
        session: Session,
        start_date: date,
        end_date: date,
        type: VacationType | None = None,
    ) -> set[EmployeeModel]:
        vacations = self.repository.get_many(
            session,
            self.repository.model.start_date <= end_date,
            self.repository.model.end_date >= start_date,
            self.repository.model.type == type if type else True,
        )
        return {v.employee for v in vacations}

    def get_vacation_number_of_workdays(
        self, vacation: VacationCreate | VacationModel
    ) -> int:
        """
        Get the number of workdays in the given vacation.
        Without counting public holidays and weekends.
        """

        # ? For now, timezone can only be France
        calendar = get_calendar_for_tz("Europe/Paris")

        return calendar.get_working_days_delta(vacation.start_date, vacation.end_date)  # type: ignore


VacationService = _VacationService(validators=[OverlappingVacationTypeValidator])
