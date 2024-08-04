import unittest
from tests.test_classes import Person, Address
from transmutate.jsonb_handler import JSONBHandler


class TestJSONBHandler(unittest.TestCase):
    def setUp(self):
        # Set up a Person object for testing
        self.person = Person(
            name="John Doe",
            age=30,
            email="john.doe@example.com",
            phone_numbers=["123-456-7890"],
        )

        # Set up an Address object for testing
        self.address = Address(
            street="123 Main St",
            city="Anytown",
            zip_code="12345",
        )

    def test_to_jsonb_person(self):
        # Test JSONB serialization for the Person dataclass
        jsonb_handler = JSONBHandler(self.person)
        jsonb_content = jsonb_handler.to_jsonb()

        expected_jsonb = '{"name":"John Doe","age":30,"email":"john.doe@example.com","phone_numbers":["123-456-7890"]}'
        self.assertEqual(jsonb_content, expected_jsonb)

    def test_to_jsonb_address(self):
        # Test JSONB serialization for the Address dataclass
        jsonb_handler = JSONBHandler(self.address)
        jsonb_content = jsonb_handler.to_jsonb()

        expected_jsonb = '{"street":"123 Main St","city":"Anytown","zip_code":"12345"}'
        self.assertEqual(jsonb_content, expected_jsonb)

    def test_parse_jsonb_person(self):
        # Test JSONB deserialization for the Person dataclass
        jsonb_data = '{"name":"John Doe","age":30,"email":"john.doe@example.com","phone_numbers":["123-456-7890"]}'
        data_dict = JSONBHandler.parse_jsonb(jsonb_data)

        self.assertEqual(data_dict["name"], "John Doe")
        self.assertEqual(data_dict["age"], 30)
        self.assertEqual(data_dict["email"], "john.doe@example.com")
        self.assertEqual(data_dict["phone_numbers"], ["123-456-7890"])

    def test_parse_jsonb_address(self):
        # Test JSONB deserialization for the Address dataclass
        jsonb_data = '{"street":"123 Main St","city":"Anytown","zip_code":"12345"}'
        data_dict = JSONBHandler.parse_jsonb(jsonb_data)

        self.assertEqual(data_dict["street"], "123 Main St")
        self.assertEqual(data_dict["city"], "Anytown")
        self.assertEqual(data_dict["zip_code"], "12345")


if __name__ == "__main__":
    unittest.main()
