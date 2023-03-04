from app.model import VacationModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository[VacationModel]):
    ...


VacationRepository = _VacationRepository(model=VacationModel)
