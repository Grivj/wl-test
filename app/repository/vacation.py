from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.model import EmployeeModel, VacationModel
from app.repository.base import BaseRepository
from app.schema.vacation import VacationCreate, VacationType


class _VacationRepository(BaseRepository[VacationModel]):
    def get_overlapping_vacations(
        self, session: Session, vacation: VacationCreate
    ) -> list[VacationModel]:
        """
        Returns a list of vacations that overlap or contiguously touch the given
        vacation.
        """
        return self.get_many(
            session,
            self.model.employee_id == vacation.employee_id,
            self.model.start_date <= vacation.end_date + timedelta(days=1),
            self.model.end_date >= vacation.start_date - timedelta(days=1),
        )

    def get_employee_vacations(
        self,
        session: Session,
        employee: EmployeeModel,
        start_date: date,
        end_date: date,
        type: VacationType | None = None,
    ) -> list[VacationModel]:
        return self.get_many(
            session,
            self.model.employee_id == employee.id,
            self.model.start_date <= end_date,
            self.model.end_date >= start_date,
            self.model.type == type if type else True,
        )


VacationRepository = _VacationRepository(model=VacationModel)
