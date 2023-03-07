from uuid import UUID

import pytz
from pydantic import BaseModel, Field, validator


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    timezone: str = Field(default="Europe/Paris")
    team_id: UUID | None = None

    @validator("timezone")
    def validate_timezone(cls, v: str) -> str:
        # ? locking the timezone to Europe/Paris for now
        if v != "Europe/Paris":
            raise ValueError("Only Europe/Paris is supported for now")
        # ? bypassed for now
        if v not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {v}")
        return v


class EmployeeCreate(EmployeeBase):
    ...


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class EmployeeInDB(EmployeeBase):
    id: UUID

    class Config:
        orm_mode = True


class Employee(EmployeeInDB):
    ...
