from sqlalchemy.orm import Session

from app.model import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository[EmployeeModel]):
    def get_by_id(self, session: Session, employee_id: int) -> EmployeeModel | None:
        return self.get(session, id=employee_id)


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
