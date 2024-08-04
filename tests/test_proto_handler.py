import unittest
from tests.test_classes import Person, Address
from transmutate.proto_handler import ProtoHandler


class TestProtoHandler(unittest.TestCase):
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

    def test_generate_proto_person(self):
        # Test Proto generation for the Person dataclass
        proto_handler = ProtoHandler(self.person)
        proto_content = proto_handler.generate_proto()

        expected_person_proto = """syntax = "proto3";

message Person {
  string name = 1;
  int32 age = 2;
  string email = 3;
  repeated string phone_numbers = 4;
}"""

        self.assertIn(expected_person_proto, proto_content)

    def test_generate_proto_address(self):
        # Test Proto generation for the Address dataclass
        proto_handler = ProtoHandler(self.address)
        proto_content = proto_handler.generate_proto()

        expected_address_proto = """syntax = "proto3";

message Address {
  string street = 1;
  string city = 2;
  string zip_code = 3;
}"""

        self.assertIn(expected_address_proto, proto_content)

    def test_proto_syntax(self):
        # Test that the Proto syntax is correct
        proto_handler = ProtoHandler(self.person)
        proto_content = proto_handler.generate_proto()

        # Check for correct syntax at the start of the Proto file
        self.assertTrue(proto_content.startswith('syntax = "proto3";\n\n'))
        self.assertIn("message Person {", proto_content)

    def test_field_types(self):
        # Test that field types are correctly converted
        proto_handler = ProtoHandler(self.person)
        proto_content = proto_handler.generate_proto()

        # Check that fields have correct Proto types
        self.assertIn("string name", proto_content)
        self.assertIn("int32 age", proto_content)
        self.assertIn("repeated string phone_numbers", proto_content)

    def test_field_order(self):
        # Test that fields are in the correct order
        proto_handler = ProtoHandler(self.person)
        proto_content = proto_handler.generate_proto()

        expected_order = """string name = 1;
  int32 age = 2;
  string email = 3;
  repeated string phone_numbers = 4;"""

        self.assertIn(expected_order, proto_content)


if __name__ == "__main__":
    unittest.main()
