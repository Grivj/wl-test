from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.model import VacationModel
from app.repository.base import BaseRepository
from app.schema.vacation import VacationCreate


class _VacationRepository(BaseRepository[VacationModel]):
    def get_overlapping_vacations(
        self, session: Session, vacation: VacationCreate
    ) -> list[VacationModel]:
        """Returns a list of vacations that overlap with the given vacation."""
        return self.get_many(
            session,
            self.model.employee_id == vacation.employee_id,
            self.model.type == vacation.type,
            self.model.start_date <= vacation.end_date,
            self.model.end_date >= vacation.start_date,
        )

    def merge_vacations(
        self, session: Session, overlapping_vacations: list[VacationModel]
    ) -> None:
        ...


VacationRepository = _VacationRepository(model=VacationModel)
