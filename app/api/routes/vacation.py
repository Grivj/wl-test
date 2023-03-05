from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_employee_by_id
from app.db.session import get_db
from app.model import EmployeeModel
from app.repository.vacation import VacationRepository
from app.schema.vacation import Vacation

router = APIRouter()


@router.get("/{employee_id}", response_model=list[Vacation])
def get_employee_vacations(
    employee: EmployeeModel = Depends(get_employee_by_id), db: Session = Depends(get_db)
) -> list[Vacation]:
    return [
        Vacation.from_orm(model)
        for model in VacationRepository.get_many(db, employee_id=employee.id)
    ]
