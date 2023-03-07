from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.model import EmployeeModel, VacationModel
from app.repository.base import BaseRepository
from app.schema.vacation import VacationCreate, VacationType
from app.serializers import Serializer


class VacationRepository(BaseRepository[VacationModel]):
    serializer = Serializer(VacationModel)

    def create_vacation(
        self, session: Session, vacation: VacationCreate
    ) -> VacationModel:
        model = self.serializer.deserialize(vacation)
        return self.create(session, model)

    def get_vacation_by_id(self, session: Session, id: int) -> VacationModel | None:
        return self.get(session, id=id)

    def delete_vacation(self, session: Session, vacation: VacationModel) -> None:
        self.delete(session, vacation)

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
        start_date: date | None = None,
        end_date: date | None = None,
        type: VacationType | None = None,
    ) -> list[VacationModel]:
        if not start_date and not end_date:
            return self.get_many(
                session,
                self.model.employee_id == employee.id,
                self.model.type == type if type else True,
            )
        if not start_date:
            return self.get_many(
                session,
                self.model.employee_id == employee.id,
                self.model.end_date <= end_date,
                self.model.type == type if type else True,
            )
        return (
            self.get_many(
                session,
                self.model.employee_id == employee.id,
                self.model.start_date <= end_date,
                self.model.end_date >= start_date,
                self.model.type == type if type else True,
            )
            if end_date
            else self.get_many(
                session,
                self.model.employee_id == employee.id,
                self.model.start_date >= start_date,
                self.model.type == type if type else True,
            )
        )
