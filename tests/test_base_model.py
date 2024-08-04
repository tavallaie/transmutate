import unittest
from tests.test_classes import Person, Address


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.address = Address(street="123 Main St", city="Anytown", zip_code="12345")
        self.person = Person(
            name="John Doe",
            age=30,
            email="john.doe@example.com",
            phone_numbers=["123-456-7890"],
            address=self.address,
        )

    def test_to_json(self):
        json_content = self.person.to_json()
        self.assertIn('"name": "John Doe"', json_content)
        self.assertIn('"age": 30', json_content)
        self.assertIn('"street": "123 Main St"', json_content)

    def test_to_jsonb(self):
        jsonb_content = self.person.to_jsonb()
        self.assertIn('"name":"John Doe"', jsonb_content)
        self.assertIn('"age":30', jsonb_content)
        self.assertIn('"street":"123 Main St"', jsonb_content)

    def test_from_json(self):
        json_data = '{"name": "John Doe", "age": 30, "email": "john.doe@example.com", "phone_numbers": ["123-456-7890"], "address": {"street": "123 Main St", "city": "Anytown", "zip_code": "12345"}}'
        person_from_json = Person.from_json(json_data)
        self.assertEqual(person_from_json.name, "John Doe")
        self.assertEqual(person_from_json.age, 30)
        self.assertEqual(person_from_json.address.city, "Anytown")

    def test_from_jsonb(self):
        jsonb_data = '{"name":"Jane Doe","age":28,"email":"jane.doe@example.com","phone_numbers":["555-555-5555"],"address":{"street":"456 Elm St","city":"Othertown","zip_code":"67890"}}'
        person_from_jsonb = Person.from_jsonb(jsonb_data)
        self.assertEqual(person_from_jsonb.name, "Jane Doe")
        self.assertEqual(person_from_jsonb.age, 28)
        self.assertEqual(person_from_jsonb.address.zip_code, "67890")

    def test_invalid_age(self):
        with self.assertRaises(ValueError) as context:
            Person(name="John Doe", age=130, email="john.doe@example.com")
        self.assertEqual(str(context.exception), "Age must be between 0 and 120.")

    def test_invalid_email(self):
        with self.assertRaises(ValueError) as context:
            Person(name="John Doe", age=30, email="john.doeexample.com")
        self.assertEqual(str(context.exception), "Invalid email address.")

    def test_invalid_zip_code(self):
        with self.assertRaises(ValueError) as context:
            Address(street="123 Main St", city="Anytown", zip_code="1234")
        self.assertEqual(str(context.exception), "Zip code must be a 5-digit number.")


if __name__ == "__main__":
    unittest.main()
