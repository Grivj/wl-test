from uuid import UUID

from sqlalchemy.orm import Session

from app.model import TeamModel
from app.repository.base import BaseRepository
from app.schema.team import TeamCreate, TeamUpdate
from app.serializers import Serializer


class TeamRepository(BaseRepository[TeamModel]):
    serializer = Serializer(TeamModel)

    def create_team(self, session: Session, team: TeamCreate) -> TeamModel:
        model = self.serializer.deserialize(team)
        return self.create(session, model)

    def get_team_by_id(self, session: Session, id: UUID) -> TeamModel | None:
        return self.get(session, id=id)

    def delete_team(self, session: Session, team: TeamModel) -> None:
        self.delete(session, team)

    def update_team(
        self, session: Session, team: TeamModel, data: TeamUpdate
    ) -> TeamModel:
        for field in data.dict(exclude_unset=True):
            setattr(team, field, getattr(data, field))
        self.update(session, team)
        return team

    def get_team_by_name(self, session: Session, name: str) -> TeamModel | None:
        return (
            session.query(self.model)  # type: ignore
            .filter(self.model.name.ilike(name))  # type: ignore
            .one_or_none()
        )
