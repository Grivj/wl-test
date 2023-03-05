from uuid import UUID

from pydantic import BaseModel


class BalanceBase(BaseModel):
    balance: int
    employee_id: UUID


class BalanceCreate(BalanceBase):
    ...


class Balance(BalanceBase):
    id: UUID

    class Config:
        orm_mode = True
