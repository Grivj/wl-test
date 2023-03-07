import unittest
from uuid import UUID

from app.model.employee import EmployeeModel
from app.schema.employee import Employee
from app.serializers import Serializer


class TestSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = Serializer(EmployeeModel)

        self.dummy_employee_schema = Employee(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            first_name="John",
            last_name="Doe",
        )
        self.dummy_employee_model = EmployeeModel(**self.dummy_employee_schema.dict())

    def test_serialize(self):
        # test serialization of single employee
        schema = Employee
        serialized = self.serializer.serialize(self.dummy_employee_model, schema)
        expected = schema.from_orm(self.dummy_employee_schema)
        self.assertEqual(serialized, expected)

        # test serialization of multiple employees
        employees = [self.dummy_employee_model]
        serialized = self.serializer.serialize_many(employees, schema)
        expected = [schema.from_orm(self.dummy_employee_schema)]
        self.assertEqual(serialized, expected)

    def test_deserialize(self):
        # test deserialization of single employee
        deserialized = self.serializer.deserialize(self.dummy_employee_schema)
        self.assertIsInstance(deserialized, EmployeeModel)

        # test deserialization of multiple employees
        data_list = [self.dummy_employee_schema]
        deserialized = self.serializer.deserialize_many(data_list)
        self.assertIsInstance(deserialized, list)
        self.assertIsInstance(deserialized[0], EmployeeModel)
