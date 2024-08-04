import unittest
import os
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

        self.assertEqual(proto_content.strip(), expected_person_proto.strip())

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

        self.assertEqual(proto_content.strip(), expected_address_proto.strip())

    def test_write_proto_file_person(self):
        # Test writing the Proto content to a file for the Person dataclass
        proto_handler = ProtoHandler(self.person)
        filename = "person_test.proto"

        # Write the Proto to a file
        proto_handler.write_proto_file(filename)

        # Verify the file exists
        self.assertTrue(os.path.exists(filename))

        # Read the file and verify its content
        with open(filename, "r") as file:
            file_content = file.read()

        expected_content = """syntax = "proto3";

message Person {
  string name = 1;
  int32 age = 2;
  string email = 3;
  repeated string phone_numbers = 4;
}"""

        self.assertEqual(file_content.strip(), expected_content.strip())

        # Clean up by removing the created file
        os.remove(filename)

    def test_write_proto_file_address(self):
        # Test writing the Proto content to a file for the Address dataclass
        proto_handler = ProtoHandler(self.address)
        filename = "address_test.proto"

        # Write the Proto to a file
        proto_handler.write_proto_file(filename)

        # Verify the file exists
        self.assertTrue(os.path.exists(filename))

        # Read the file and verify its content
        with open(filename, "r") as file:
            file_content = file.read()

        expected_content = """syntax = "proto3";

message Address {
  string street = 1;
  string city = 2;
  string zip_code = 3;
}"""

        self.assertEqual(file_content.strip(), expected_content.strip())

        # Clean up by removing the created file
        os.remove(filename)


if __name__ == "__main__":
    unittest.main()
