from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.model import VacationModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository[VacationModel]):
    def get_overlapping_vacations(
        self, session: Session, employee_id: UUID, start_date: date, end_date: date
    ) -> list[VacationModel]:
        return self.get_many(
            session,
            self.model.employee_id == employee_id,
            self.model.start_date <= end_date,
            self.model.end_date >= start_date,
        )


VacationRepository = _VacationRepository(model=VacationModel)
