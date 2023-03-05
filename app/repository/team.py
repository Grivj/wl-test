from sqlalchemy.orm import Session

from app.model import TeamModel
from app.repository.base import BaseRepository


class _TeamRepository(BaseRepository[TeamModel]):
    def get_by_name(self, session: Session, name: str) -> TeamModel | None:
        return (
            session.query(self.model)  # type: ignore
            .filter(self.model.name.ilike(name))  # type: ignore
            .one_or_none()
        )


TeamRepository = _TeamRepository(model=TeamModel)
