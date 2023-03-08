from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.model import EmployeeModel, VacationModel
from app.repository.balance import BalanceRepository
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate, VacationType

from .vacation_validators import OverlappingVacationTypeValidator, get_calendar_for_tz


@dataclass
class VacationService:
    repository: VacationRepository
    balance_repository: BalanceRepository
    domain_service: VacationDomainService

    def create_vacation(
        self, session: Session, vacation: VacationCreate
    ) -> VacationModel:
        return self.domain_service.create_vacation(
            session, vacation, self.repository, self.balance_repository
        )

    def update(
        self,
        session: Session,
        old_vacation: VacationModel,
        new_vacation: VacationCreate,
    ) -> VacationModel:
        return self.domain_service.update_vacation(
            session,
            old_vacation,
            new_vacation,
            self.repository,
            self.balance_repository,
        )

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


@dataclass
class VacationDomainService:
    def create_vacation(
        self,
        session: Session,
        vacation: VacationCreate,
        repository: VacationRepository,
        balance_repository: BalanceRepository,
    ) -> VacationModel:
        overlapping_vacations = repository.get_overlapping_vacations(session, vacation)
        self.validate_overlapping_vacations(session, vacation, overlapping_vacations)
        if overlapping_vacations:
            return self.handle_overlapping_vacations(
                session, vacation, overlapping_vacations, repository, balance_repository
            )
        return self.create_and_update_vacation_balance(
            session=session,
            vacation=vacation,
            repository=repository,
            balance_repository=balance_repository,
        )

    def update_vacation(
        self,
        session: Session,
        old_vacation: VacationModel,
        new_vacation: VacationCreate,
        repository: VacationRepository,
        balance_repository: BalanceRepository,
    ) -> VacationModel:
        overlapping_vacations = repository.get_overlapping_vacations(
            session, new_vacation
        )
        overlapping_vacations = [
            v for v in overlapping_vacations if v.id != old_vacation.id
        ]
        self.validate_overlapping_vacations(
            session, new_vacation, overlapping_vacations
        )
        if not self.can_employee_take_vacation(
            session, old_vacation.employee, new_vacation, balance_repository
        ):
            raise ValueError(
                f"Employee with id {old_vacation.employee.id} does not have enough balance to take this vacation."
            )
        if overlapping_vacations:
            return self.handle_overlapping_vacations(
                session=session,
                vacation=new_vacation,
                overlapping_vacations=overlapping_vacations,
                repository=repository,
                balance_repository=balance_repository,
            )
        return repository.update(
            session,
            VacationModel(employee=old_vacation.employee, **new_vacation.dict()),  # type: ignore
        )

    def validate_overlapping_vacations(
        self,
        session: Session,
        vacation: VacationCreate,
        overlapping_vacations: list[VacationModel],
    ):
        validators = [OverlappingVacationTypeValidator()]
        for validator in validators:
            validator.validate(
                session, vacation=vacation, overlapping_vacations=overlapping_vacations
            )

    def handle_overlapping_vacations(
        self,
        session: Session,
        vacation: VacationCreate,
        overlapping_vacations: list[VacationModel],
        repository: VacationRepository,
        balance_repository: BalanceRepository,
    ) -> VacationModel:
        merged_vacation = self.merge_vacations(vacation, overlapping_vacations)
        repository.delete_many(session, overlapping_vacations)
        return self.create_and_update_vacation_balance(
            session=session,
            vacation=merged_vacation,
            repository=repository,
            balance_repository=balance_repository,
        )

    def create_and_update_vacation_balance(
        self,
        session: Session,
        vacation: VacationCreate,
        repository: VacationRepository,
        balance_repository: BalanceRepository,
    ):
        created_vacation = repository.create_vacation(session, vacation)
        self.update_balance_by_vacation(session, created_vacation, balance_repository)
        return created_vacation

    def update_balance_by_vacation(
        self,
        session: Session,
        vacation: VacationModel,
        balance_repository: BalanceRepository,
    ):
        vacation_cost = self.get_vacation_number_of_workdays(vacation)
        balance_repository.update_balance(session, vacation.employee, vacation_cost)

    def merge_vacations(
        self, vacation: VacationCreate, overlapping_vacations: list[VacationModel]
    ) -> VacationCreate:
        start_date = min(v.start_date for v in overlapping_vacations)
        end_date = max(v.end_date for v in overlapping_vacations)
        vacation.start_date = min(vacation.start_date, start_date)
        vacation.end_date = max(vacation.end_date, end_date)
        return vacation

    def get_vacation_number_of_workdays(
        self, vacation: VacationCreate | VacationModel
    ) -> int:
        calendar = get_calendar_for_tz("Europe/Paris")
        return calendar.get_working_days_delta(vacation.start_date, vacation.end_date)  # type: ignore

    def can_employee_take_vacation(
        self,
        session: Session,
        employee: EmployeeModel,
        vacation: VacationCreate,
        balance_repository: BalanceRepository,
    ):
        vacation_cost = self.get_vacation_number_of_workdays(vacation)
        current_balance = balance_repository.get_by_employee_id(session, employee.id)
        if current_balance is None:
            # ? Handle differently later
            raise EmployeeHasNoBalanceException("No balance found for employee")
        return current_balance.balance >= vacation_cost


class EmployeeHasNoBalanceException(Exception):
    pass
