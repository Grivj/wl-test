from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.model import EmployeeModel
from app.repository.employee import EmployeeRepository


def get_employee_by_id(
    db: Session = Depends(get_db), *, employee_id: UUID
) -> EmployeeModel:
    """Returns an employee by id or raises an HTTPException if not found."""
    if not (employee := EmployeeRepository.get_by_id(db, employee_id)):
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
