import unittest
from tests.test_classes import Person, Address
from transmutate.json_handler import JSONHandler


class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        address = Address(street="123 Main St", city="Anytown", zip_code="12345")
        self.person = Person(
            name="John Doe",
            age=30,
            email="john.doe@example.com",
            phone_numbers=["123-456-7890"],
            address=address,
        )

    def test_to_json(self):
        json_handler = JSONHandler(self.person)
        json_content = json_handler.to_json()
        self.assertIn('"name": "John Doe"', json_content)
        self.assertIn('"age": 30', json_content)
        self.assertIn('"street": "123 Main St"', json_content)


if __name__ == "__main__":
    unittest.main()
