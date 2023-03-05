from typing import Protocol

from app.model.vacation import VacationModel


class VacationValidator(Protocol):
    def validate(self, vacation: VacationModel) -> bool:
        ...


class OverlappingVacationValidator:
    def validate(self, vacation: VacationModel) -> bool:
        ...