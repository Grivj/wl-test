from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel, CustomUUID
from .employee import EmployeeModel


class BalanceModel(BaseModel):
    __tablename__ = "balance"

    employee_id = Column(CustomUUID, ForeignKey("employee.id"), nullable=False)
    # ? we start with a top-up of 10 days
    # ? obviously for testing purposes
    # ? and shouldn't be done that way in production
    balance = Column(Integer, default=10)

    employee: "relationship[EmployeeModel]" = relationship(
        "EmployeeModel", back_populates="balance"
    )
