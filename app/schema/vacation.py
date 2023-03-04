from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class VacationType(StrEnum):
    UNPAID = "unpaid"
    PAID = "paid"


class VacationBase(BaseModel):
    employee_id: UUID
    end_date: date
    start_date: date
    type: VacationType


class VacationCreate(VacationBase):
    ...


class Vacation(VacationBase):
    id: UUID

    class Config:
        orm_mode = True
