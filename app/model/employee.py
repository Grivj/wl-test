from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BaseModel, CustomUUID


class EmployeeModel(BaseModel):
    __tablename__ = "employee"

    first_name = Column(String)
    last_name = Column(String)
    timezone = Column(String, default="Europe/Paris")

    team_id = Column(CustomUUID, ForeignKey("team.id"), nullable=True)
    # ? should be of type relationship[TeamModel]
    # ? removed to avoid circular import for now
    team = relationship("TeamModel", back_populates="employees")  # type: ignore
    vacations = relationship("VacationModel", back_populates="employee")  # type: ignore
    balance = relationship("BalanceModel", back_populates="employee")  # type: ignore
