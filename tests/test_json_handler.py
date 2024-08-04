import unittest
from tests.test_classes import Person, Address
from transmutate.json_handler import JSONHandler


class TestJSONHandler(unittest.TestCase):
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

    def test_to_json_person(self):
        # Test JSON serialization for the Person dataclass
        json_handler = JSONHandler(self.person)
        json_content = json_handler.to_json()

        expected_json = """{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "phone_numbers": [
        "123-456-7890"
    ]
}"""
        self.assertEqual(json_content, expected_json)

    def test_to_json_address(self):
        # Test JSON serialization for the Address dataclass
        json_handler = JSONHandler(self.address)
        json_content = json_handler.to_json()

        expected_json = """{
    "street": "123 Main St",
    "city": "Anytown",
    "zip_code": "12345"
}"""
        self.assertEqual(json_content, expected_json)

    def test_parse_json_person(self):
        # Test JSON deserialization for the Person dataclass
        json_data = '{"name": "John Doe", "age": 30, "email": "john.doe@example.com", "phone_numbers": ["123-456-7890"]}'
        data_dict = JSONHandler.parse_json(json_data)

        self.assertEqual(data_dict["name"], "John Doe")
        self.assertEqual(data_dict["age"], 30)
        self.assertEqual(data_dict["email"], "john.doe@example.com")
        self.assertEqual(data_dict["phone_numbers"], ["123-456-7890"])

    def test_parse_json_address(self):
        # Test JSON deserialization for the Address dataclass
        json_data = '{"street": "123 Main St", "city": "Anytown", "zip_code": "12345"}'
        data_dict = JSONHandler.parse_json(json_data)

        self.assertEqual(data_dict["street"], "123 Main St")
        self.assertEqual(data_dict["city"], "Anytown")
        self.assertEqual(data_dict["zip_code"], "12345")


if __name__ == "__main__":
    unittest.main()
