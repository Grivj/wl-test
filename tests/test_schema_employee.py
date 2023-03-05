import unittest

from app.schema.employee import EmployeeBase


class TestEmployeeBaseSchema(unittest.TestCase):
    def test_timezone_default(self):
        self.assertEqual(
            EmployeeBase(first_name="Jerome", last_name="Powell").timezone,
            "Europe/Paris",
        )

    # ? locked to Europe/Paris for now
    # def test_timezone_set(self):
    #     self.assertEqual(
    #         EmployeeBase(
    #             first_name="Jerome", last_name="Powell", timezone="Europe/London"
    #         ).timezone,
    #         "Europe/London",
    #     )

    def test_timezone_locked_to_europe_paris(self):
        self.assertRaises(
            ValueError,
            EmployeeBase,
            first_name="Jerome",
            last_name="Powell",
            timezone="Europe/London",
        )

    def test_timezone_wrong(self):
        with self.assertRaises(ValueError):
            EmployeeBase(first_name="Jerome", last_name="Powell", timezone="Paris")
