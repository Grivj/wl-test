import unittest
from uuid import UUID

from app.model import TeamModel
from app.repository.team import TeamRepository
from app.schema.employee import Employee
from app.schema.team import TeamCreate
from tests.utils import get_test_db


class TestTeamRepository(unittest.TestCase):
    def setUp(self):
        self.session = get_test_db()
        self.repository = TeamRepository(TeamModel)

        self.dummy_team_schema = TeamCreate(name="TeamA")
        self.dummy_team_model = TeamModel(**self.dummy_team_schema.dict())
        self.dummy_employee_schema = Employee(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            first_name="John",
            last_name="Doe",
        )

    def test_create_team(self):
        # test successful creation
        team = self.repository.create_team(self.session, self.dummy_team_schema)
        self.assertEqual(team.name, self.dummy_team_schema.name)

        # test get team by id
        team = self.repository.get_team_by_id(self.session, team.id)
        self.assertIsNotNone(team)
        assert team is not None
        self.assertEqual(team.name, self.dummy_team_schema.name)

    def test_get_team_by_name(self):
        # create team
        team = self.repository.create_team(self.session, self.dummy_team_schema)

        # fetch team by name
        team = self.repository.get_team_by_name(self.session, team.name)
        assert team is not None
        self.assertEqual(team.name, self.dummy_team_schema.name)
