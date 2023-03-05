from uuid import UUID

from sqlalchemy.orm import Session

from app.model import BalanceModel, EmployeeModel
from app.repository.base import BaseRepository
from app.schema.balance import BalanceCreate


class _BalanceRepository(BaseRepository[BalanceModel]):
    def create_for_employee(
        self, session: Session, employee: EmployeeModel, balance_amount: int = 10
    ) -> BalanceModel:
        """Creates a new balance for the given employee."""
        balance = self.model(
            **BalanceCreate(employee_id=employee.id, balance=balance_amount).dict()
        )
        return self.create(session, balance)

    def delete_by_employee_id(self, session: Session, employee_id: UUID):
        """Deletes the balance for the given employee."""
        if balance := self.get_by_employee_id(session, employee_id):
            self.delete(session, balance)

    def get_by_employee_id(
        self, session: Session, employee_id: UUID
    ) -> BalanceModel | None:
        return self.get(session, self.model.employee_id == employee_id)

    def update_balance(
        self, session: Session, employee: EmployeeModel, amount: int
    ) -> BalanceModel | None:
        """Updates the balance for the given employee."""
        if not (balance := self.get_by_employee_id(session, employee.id)):
            return
        balance.balance += amount  # type: ignore
        self.update(session, balance)
        return balance


BalanceRepository = _BalanceRepository(model=BalanceModel)
