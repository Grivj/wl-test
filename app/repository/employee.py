from uuid import UUID

from sqlalchemy.orm import Session

from app.model import EmployeeModel, TeamModel
from app.repository.base import BaseRepository
from app.schema.employee import EmployeeCreate, EmployeeUpdate
from app.serializers import Serializer


class EmployeeRepository(BaseRepository[EmployeeModel]):
    serializer = Serializer(EmployeeModel)

    def create_employee(
        self, session: Session, employee: EmployeeCreate
    ) -> EmployeeModel:
        model = self.serializer.deserialize(employee)
        return self.create(session, model)

    def get_employee_by_id(self, session: Session, id: UUID) -> EmployeeModel | None:
        return self.get(session, id=id)

    def delete_employee(self, session: Session, employee: EmployeeModel) -> None:
        self.delete(session, employee)

    def update_employee(
        self, session: Session, employee: EmployeeModel, data: EmployeeUpdate
    ) -> EmployeeModel:
        for field in data.dict(exclude_unset=True):
            setattr(employee, field, getattr(data, field))
        self.update(session, employee)
        return employee

    def update_team(
        self, session: Session, employee: EmployeeModel, team: TeamModel
    ) -> None:
        # if the employee is already in the team, raise an error
        if employee.team_id == team.id:
            raise ValueError(
                f"Employee with id {employee.id} is already in team {team.name}"
            )

        employee.team_id = team.id  # type: ignore
        self.update(session, employee)

    def remove_team(self, session: Session, employee: EmployeeModel) -> None:
        employee.team_id = None  # type: ignore
        self.update(session, employee)
