import unittest
from tests.test_classes import Person, Address
from transmutate.jsonb_handler import JSONBHandler


class TestJSONBHandler(unittest.TestCase):
    def setUp(self):
        address = Address(street="123 Main St", city="Anytown", zip_code="12345")
        self.person = Person(
            name="John Doe",
            age=30,
            email="john.doe@example.com",
            phone_numbers=["123-456-7890"],
            address=address,
        )

    def test_to_jsonb(self):
        jsonb_handler = JSONBHandler(self.person)
        jsonb_content = jsonb_handler.to_jsonb()
        self.assertIn('"name":"John Doe"', jsonb_content)
        self.assertIn('"age":30', jsonb_content)
        self.assertIn('"street":"123 Main St"', jsonb_content)


if __name__ == "__main__":
    unittest.main()
