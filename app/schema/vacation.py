from datetime import date
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, validator


class VacationType(StrEnum):
    UNPAID = "unpaid"
    PAID = "paid"


class VacationBase(BaseModel):
    start_date: date
    end_date: date
    employee_id: UUID
    type: VacationType = VacationType.PAID

    @validator("end_date")
    def validate_end_date(cls, v: date, values: dict[str, Any]) -> date:
        """End date must be greater or equal to start date."""
        if v < values["start_date"]:
            raise ValueError("End date must be greater or equal to start date")
        return v


class VacationCreate(VacationBase):
    ...


class VacationUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    employee_id: UUID | None = None
    type: VacationType | None = None


class VacationInDB(VacationBase):
    id: UUID

    class Config:
        orm_mode = True


class Vacation(VacationInDB):
    ...
