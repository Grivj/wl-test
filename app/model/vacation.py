from sqlalchemy import Column, Date, Enum, ForeignKey

from app.schema.vacation import VacationType

from .base import BaseModel, CustomUUID


class VacationModel(BaseModel):
    __tablename__ = "vacation"

    employee_id = Column(CustomUUID, ForeignKey("employee.id"), nullable=False)
    end_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    type = Column(Enum(VacationType), nullable=False)
