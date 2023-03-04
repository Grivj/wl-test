from uuid import UUID

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str


class EmployeeCreate(EmployeeBase):
    ...


class Employee(EmployeeBase):
    id: UUID

    class Config:
        orm_mode = True
