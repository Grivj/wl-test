from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.model import EmployeeModel
from app.repository.balance import BalanceRepository
from app.repository.employee import EmployeeRepository
from app.schema.employee import EmployeeCreate


@dataclass
class EmployeeService:
    session: Session
    repository: EmployeeRepository
    balance_repository: BalanceRepository

    def create_employee(
        self,
        employee_create: EmployeeCreate,
        balance_amount: int = 10,
    ) -> EmployeeModel:
        employee = self.repository.create_employee(self.session, employee_create)
        self.balance_repository.create_for_employee(
            self.session, employee, balance_amount
        )
        return employee

    def delete_employee(self, employee: EmployeeModel):
        self.balance_repository.delete_by_employee_id(self.session, employee.id)
        self.repository.delete_employee(self.session, employee)

    def get_employee(self, employee_id: UUID) -> EmployeeModel:
        if not (
            employee := self.repository.get_employee_by_id(self.session, employee_id)
        ):
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
