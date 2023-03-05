from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.model import EmployeeModel
from app.repository.balance import BalanceRepository
from app.repository.employee import EmployeeRepository
from app.schema.employee import EmployeeCreate


@dataclass
class _EmployeeService:
    repository = EmployeeRepository
    balance_repository = BalanceRepository

    def create_with_balance(
        self,
        session: Session,
        employee_create: EmployeeCreate,
        balance_amount: int = 10,
    ) -> EmployeeModel:
        employee = self.repository.create(session, employee_create.dict())
        self.balance_repository.create_for_employee(session, employee, balance_amount)
        return employee

    def delete(self, session: Session, employee: EmployeeModel):
        self.balance_repository.delete_by_employee_id(session, employee.id)
        self.repository.delete(session, employee)


EmployeeService = _EmployeeService()
