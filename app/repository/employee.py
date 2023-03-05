from sqlalchemy.orm import Session

from app.model import EmployeeModel, TeamModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository[EmployeeModel]):
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


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
