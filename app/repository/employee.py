from uuid import UUID

from sqlalchemy.orm import Session

from app.model import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository[EmployeeModel]):
    def update_team(
        self, session: Session, employee_id: UUID, team_id: UUID | None = None
    ) -> None:
        if not (employee := self.get_by_id(session, employee_id)):
            raise ValueError(f"Employee with id {employee_id} not found")
        # if the employee is already in the team, raise an error
        if team_id and employee.team_id == team_id:
            raise ValueError(
                f"Employee with id {employee_id} is already in team {team_id}"
            )

        employee.team_id = team_id  # type: ignore
        self.update(session, employee)


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
