from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel
from .employee import EmployeeModel


class TeamModel(BaseModel):
    __tablename__ = "team"

    name = Column(String, unique=True, index=True)
    employees: "relationship[list[EmployeeModel]]" = relationship("EmployeeModel", back_populates="team")  # type: ignore[assignment]
