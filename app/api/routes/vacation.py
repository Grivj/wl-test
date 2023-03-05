from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_employee_by_id, get_vacation_by_id
from app.db.session import get_db
from app.model import EmployeeModel, VacationModel
from app.repository.vacation import VacationRepository
from app.schema.vacation import Vacation, VacationCreate
from app.service.vacation import VacationService

router = APIRouter()


@router.get("/{employee_id}", response_model=list[Vacation])
def get_employee_vacations(
    employee: EmployeeModel = Depends(get_employee_by_id), db: Session = Depends(get_db)
) -> list[Vacation]:
    return [
        Vacation.from_orm(model)
        for model in VacationRepository.get_many(db, employee_id=employee.id)
    ]


@router.post("/{employee_id}", response_model=Vacation)
def create_employee_vacation(
    *,
    db: Session = Depends(get_db),
    employee: EmployeeModel = Depends(get_employee_by_id),
    vacation: VacationCreate,
) -> Vacation:
    # check that the employee id in the path matches the employee id in the body
    if employee.id != vacation.employee_id:
        raise HTTPException(
            status_code=400,
            detail=f"Employee id in path ({employee.id}) does not match employee id in body ({vacation.employee_id})",
        )
    try:
        return Vacation.from_orm(VacationService.create(db, vacation))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{employee_id}/vacations/{vacation_id}", status_code=status.HTTP_200_OK)
async def delete_vacation(
    *,
    db: Session = Depends(get_db),
    employee: EmployeeModel = Depends(get_employee_by_id),
    vacation: VacationModel = Depends(get_vacation_by_id),
):
    VacationRepository.delete(db, vacation)
    return {"message": "Vacation deleted"}


@router.put("/{employee_id}/vacations/{vacation_id}", status_code=status.HTTP_200_OK)
def update_vacation(
    *,
    db: Session = Depends(get_db),
    employee: EmployeeModel = Depends(get_employee_by_id),
    vacation: VacationModel = Depends(get_vacation_by_id),
    vacation_update: VacationCreate,
):
    VacationService.update(db, vacation, vacation_update)
    return {"message": "Vacation updated"}
