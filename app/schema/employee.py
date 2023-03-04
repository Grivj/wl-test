from uuid import UUID

import pytz
from pydantic import BaseModel, validator


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    timezone: str = "Europe/Paris"
    team_id: UUID | None = None

    @validator("timezone")
    def validate_timezone(cls, v: str) -> str:
        if v not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {v}")
        return v


class EmployeeCreate(EmployeeBase):
    ...


class Employee(EmployeeBase):
    id: UUID

    class Config:
        orm_mode = True
