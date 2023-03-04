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

        employee.team_id = team_id
        self.update(session, employee)


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
