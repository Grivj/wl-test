from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class TeamModel(BaseModel):
    __tablename__ = "team"

    name = Column(String, unique=True, index=True)
    # should be of type relationship[EmployeeModel]
    # removed to avoid circular import for now
    employees = relationship("EmployeeModel", back_populates="team")  # type: ignore[assignment]
