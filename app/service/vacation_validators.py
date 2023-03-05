from typing import Protocol

from workalendar.core import Calendar
from workalendar.europe import France

from app.model.vacation import VacationModel
from app.schema.vacation import VacationCreate


def get_calendar_for_tz(tz: str) -> Calendar:
    """
    Return a calendar for the given timezone.
    For now, only France is supported.
    """
    match tz:
        case "Europe/Paris":
            return France()
        case _:
            raise ValueError(f"Timezone {tz} not supported yet")


class VacationValidator(Protocol):
    def validate(self, *args: ..., **kwargs: ...) -> None:
        ...


class OverlappingVacationTypeValidator:
    def validate(self, *args: ..., **kwargs: ...) -> None:
        vacation: VacationCreate = kwargs["vacation"]
        overlapping_vacations: list[VacationModel] = kwargs["overlapping_vacations"]
        if any(v.type != vacation.type for v in overlapping_vacations):
            raise ValueError("Vacations are of different types")
