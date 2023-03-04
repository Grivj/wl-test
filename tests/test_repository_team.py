import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.model import TeamModel
from app.repository.team import TeamRepository
from app.schema.employee import Employee
from app.schema.team import Team

DUMMY_TEAM = Team(id=UUID("00000000-0000-0000-0000-000000000001"), name="TeamA")
DUMMY_TEAM_MODEL = TeamModel(**DUMMY_TEAM.dict())
DUMMY_EMPLOYEE = Employee(
    id=UUID("00000000-0000-0000-0000-000000000001"),
    first_name="John",
    last_name="Doe",
)


class TestTeamRepository(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.repository = TeamRepository

    @patch.object(TeamRepository, "create", return_value=DUMMY_TEAM_MODEL)
    def test_create_team(self, create: MagicMock):
        obj_in = {"name": DUMMY_TEAM.name}
        response = self.repository.create(session=self.session, obj_in=obj_in)
        create.assert_called_once_with(session=self.session, obj_in=obj_in)
        assert response == DUMMY_TEAM_MODEL

    @patch.object(TeamRepository, "get", return_value=DUMMY_TEAM_MODEL)
    def test_get_team(self, get: MagicMock):
        response = self.repository.get(session=self.session, id=1)
        get.assert_called_once_with(session=self.session, id=1)
        assert response == DUMMY_TEAM_MODEL
