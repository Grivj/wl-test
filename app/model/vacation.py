from sqlalchemy import Column, Date, Enum, ForeignKey, Integer

from app.schema.vacation import VacationType

from .base import BaseModel


class VacationModel(BaseModel):
    __tablename__ = "vacation"

    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    end_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    type = Column(Enum(VacationType), nullable=False)
