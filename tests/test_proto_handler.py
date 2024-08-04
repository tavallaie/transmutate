import unittest
from tests.test_classes import Person, Address
from transmutate.proto_handler import ProtoHandler


class TestProtoHandler(unittest.TestCase):
    def setUp(self):
        address = Address(street="123 Main St", city="Anytown", zip_code="12345")
        self.person = Person(
            name="John Doe",
            age=30,
            email="john.doe@example.com",
            phone_numbers=["123-456-7890"],
            address=address,
        )

    def test_generate_proto(self):
        proto_handler = ProtoHandler(self.person)
        proto_content = proto_handler.generate_proto()
        self.assertIn("message Person", proto_content)
        self.assertIn("string name", proto_content)
        self.assertIn("int32 age", proto_content)
        self.assertIn("message Address", proto_content)
        self.assertIn("string street", proto_content)
        self.assertIn("string zip_code", proto_content)


if __name__ == "__main__":
    unittest.main()
