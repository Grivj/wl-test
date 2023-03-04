from app.model import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository[EmployeeModel]):
    ...


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
