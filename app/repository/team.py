from uuid import UUID

from sqlalchemy.orm import Session

from app.model import EmployeeModel, TeamModel
from app.repository.base import BaseRepository
from app.repository.employee import EmployeeRepository


class _TeamRepository(BaseRepository[TeamModel]):
    def get_by_name(self, session: Session, name: str) -> TeamModel | None:
        return (
            session.query(self.model)  # type: ignore
            .filter(self.model.name.ilike(name))  # type: ignore
            .one_or_none()
        )

    def get_employees(self, session: Session, team_id: UUID) -> list[EmployeeModel]:
        if not (team := self.get_by_id(session, team_id)):
            raise ValueError(f"Team with id {team_id} not found")

        return team.employees

    def add_employee(
        self, session: Session, team_id: UUID, employee_id: UUID
    ) -> TeamModel:
        if not (team := self.get_by_id(session, team_id)):
            raise ValueError(f"Team with id {team_id} not found")

        EmployeeRepository.update_team(session, employee_id, team_id)
        return team

    def remove_employee(self, session: Session, employee_id: UUID) -> None:
        EmployeeRepository.update_team(session, employee_id)


TeamRepository = _TeamRepository(model=TeamModel)
