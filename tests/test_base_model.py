import unittest
from tests.test_classes import Person, Address


class TestBaseModel(unittest.TestCase):
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

    def test_to_proto_person(self):
        # Test Proto generation for the Person dataclass
        expected_proto_content = """message Person {
  string name = 1;
  int32 age = 2;
  string email = 3;
  repeated string phone_numbers = 4;
}"""

        # Use the to_proto method to generate Proto content
        proto_content = self.person.to_proto()

        # Verify the generated content
        self.assertEqual(proto_content.strip(), expected_proto_content.strip())

    def test_to_proto_address(self):
        # Test Proto generation for the Address dataclass
        expected_proto_content = """message Address {
  string street = 1;
  string city = 2;
  string zip_code = 3;
}"""

        # Use the to_proto method to generate Proto content
        proto_content = self.address.to_proto()

        # Verify the generated content
        self.assertEqual(proto_content.strip(), expected_proto_content.strip())


if __name__ == "__main__":
    unittest.main()
