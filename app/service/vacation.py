from dataclasses import dataclass

from workalendar.core import Calendar
from workalendar.europe import France

from app.model.vacation import VacationModel

from .vacation_validators import VacationValidator


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


@dataclass
class VacationCreationService:
    validators: list[VacationValidator]

    def create_vacation(self, vacation: VacationModel) -> VacationModel:
        for validator in self.validators:
            if not validator.validate(vacation):
                raise ValueError("Vacation is not valid")

        return vacation
