from sqlalchemy import Column, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.model.employee import EmployeeModel
from app.schema.vacation import VacationType

from .base import BaseModel, CustomUUID


class VacationModel(BaseModel):
    __tablename__ = "vacation"

    employee_id = Column(CustomUUID, ForeignKey("employee.id"), nullable=False)
    end_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    type = Column(Enum(VacationType), nullable=False)

    employee: "relationship[EmployeeModel]" = relationship("EmployeeModel", back_populates="vacations")  # type: ignore[assignment]
