from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.vacation import VacationRepository
from app.schema.vacation import Vacation, VacationCreate

router = APIRouter()
