from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.model.vacation import VacationModel
from app.repository.vacation import VacationRepository
from app.schema.vacation import VacationCreate

from .vacation_validators import VacationValidator


@dataclass
class VacationService:
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
            return self.merge_vacations(session, vacation, overlapping_vacations)
        return self.repository.create(session, vacation.dict())

    def merge_vacations(
        self,
        session: Session,
        vacation: VacationCreate,
        overlapping_vacations: list[VacationModel],
    ) -> VacationModel:
        # merge the overlapping vacations into the new vacation
        start_date = min(v.start_date for v in overlapping_vacations)
        end_date = max(v.end_date for v in overlapping_vacations)
        vacation.start_date = min(vacation.start_date, start_date)
        vacation.end_date = max(vacation.end_date, end_date)
        # delete the overlapping vacations
        for v in overlapping_vacations:
            self.repository.delete(session, v)
        # create the new vacation
        return self.repository.create(session, vacation.dict())
