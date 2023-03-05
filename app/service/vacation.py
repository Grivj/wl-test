from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.model import EmployeeModel, VacationModel
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate, VacationType

from .vacation_validators import OverlappingVacationTypeValidator, VacationValidator


@dataclass
class _VacationService:
    validators: list[VacationValidator]
    repository = VacationRepository

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
        return self.repository.create(session, vacation.dict())

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
        return self.repository.update(session, VacationModel(**new_vacation.dict()))

    def handle_overlapping_vacations(
        self,
        session: Session,
        vacation: VacationCreate,
        overlapping_vacations: list[VacationModel],
    ) -> VacationModel:
        merged_vacation = self.merge_vacations(session, vacation, overlapping_vacations)
        self.repository.delete_many(session, overlapping_vacations)
        return self.repository.create(session, merged_vacation.dict())

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


VacationService = _VacationService(validators=[OverlappingVacationTypeValidator])
