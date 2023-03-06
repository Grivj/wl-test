from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_employee_by_id, get_vacation_by_id
from app.db.session import get_db
from app.model import EmployeeModel, VacationModel
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository
from app.schema.employee import Employee
from app.schema.vacation import Vacation, VacationCreate, VacationType
from app.service.vacation import VacationService
from app.service.vacation_comparison import VacationComparisonService

router = APIRouter()


@router.get("/search_employees_by_period", response_model=list[Employee])
async def search_employees_by_period(
    *,
    db: Session = Depends(get_db),
    start_date: date,
    end_date: date,
    type: VacationType | None = None,
) -> list[Employee]:
    return [
        Employee.from_orm(model)
        for model in VacationService.get_employees_in_vacation(
            db, start_date, end_date, type
        )
    ]


@router.get("/compare_employees_vacations", response_model=list[date])
async def compare_employees_vacations(
    *,
    db: Session = Depends(get_db),
    employee_1_id: UUID,
    employee_2_id: UUID,
    start_date: date,
    end_date: date,
) -> list[date]:
    if not (employee_1 := EmployeeRepository.get_by_id(db, employee_1_id)):
        raise HTTPException(
            status_code=404, detail=f"Employee {employee_1_id} not found"
        )
    if not (employee_2 := EmployeeRepository.get_by_id(db, employee_2_id)):
        raise HTTPException(
            status_code=404, detail=f"Employee {employee_2_id} not found"
        )
    return VacationComparisonService.compare_employees_vacations(
        db, employee_1, employee_2, start_date, end_date
    )


@router.get("/{employee_id}", response_model=list[Vacation])
async def get_employee_vacations(
    employee: EmployeeModel = Depends(get_employee_by_id), db: Session = Depends(get_db)
) -> list[Vacation]:
    return [
        Vacation.from_orm(model)
        for model in VacationRepository.get_many(db, employee_id=employee.id)
    ]


@router.post("/{employee_id}", response_model=Vacation)
async def create_employee_vacation(
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
async def update_vacation(
    *,
    db: Session = Depends(get_db),
    employee: EmployeeModel = Depends(get_employee_by_id),
    vacation: VacationModel = Depends(get_vacation_by_id),
    vacation_update: VacationCreate,
):
    VacationService.update(db, vacation, vacation_update)
    return {"message": "Vacation updated"}
