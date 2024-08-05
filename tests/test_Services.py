import unittest
from transmutate import BaseModel, Service, RpcType
from typing import List


class TestMessage(BaseModel):
    name: str
    age: int
    email: str
    phone_numbers: List[str]

    def to_proto(self):
        return (
            "message TestMessage {\n"
            "  string name = 1;\n"
            "  int32 age = 2;\n"
            "  string email = 3;\n"
            "  repeated string phone_numbers = 4;\n"
            "}\n"
        )


class AnotherMessage(BaseModel):
    status: str
    message: str

    def to_proto(self):
        return (
            "message AnotherMessage {\n"
            "  string status = 1;\n"
            "  string message = 2;\n"
            "}\n"
        )


class TestService(unittest.TestCase):
    def test_service_creation(self):
        # Test creation of Service object with multiple RPC types
        service = Service(
            name="TestService",
            types=[RpcType.UNARY, RpcType.SERVER_STREAMING],
            method_names=["GetInfo", "StreamInfo"],
            request_dataclass=TestMessage,
            response_dataclass=AnotherMessage,
        )
        self.assertEqual(service.name, "TestService")
        self.assertEqual(service.types, [RpcType.UNARY, RpcType.SERVER_STREAMING])
        self.assertEqual(service.method_names, ["GetInfo", "StreamInfo"])
        self.assertEqual(service.request_dataclass, TestMessage)
        self.assertEqual(service.response_dataclass, AnotherMessage)

    def test_request_message_generation(self):
        # Test Proto message generation for request dataclass
        service = Service(
            name="TestService",
            types=[RpcType.UNARY],
            method_names=["GetInfo"],
            request_dataclass=TestMessage,
        )
        proto_message = service.get_request_message()
        expected_message = (
            "message TestMessage {\n"
            "  string name = 1;\n"
            "  int32 age = 2;\n"
            "  string email = 3;\n"
            "  repeated string phone_numbers = 4;\n"
            "}\n"
        )
        self.assertEqual(proto_message.strip(), expected_message.strip())

    def test_response_message_generation(self):
        # Test Proto message generation for response dataclass
        service = Service(
            name="TestService",
            types=[RpcType.UNARY],
            method_names=["GetInfo"],
            response_dataclass=AnotherMessage,
        )
        proto_message = service.get_response_message()
        expected_message = (
            "message AnotherMessage {\n"
            "  string status = 1;\n"
            "  string message = 2;\n"
            "}\n"
        )
        self.assertEqual(proto_message.strip(), expected_message.strip())

    def test_service_definition_generation(self):
        # Test complete service definition generation
        service = Service(
            name="TestService",
            types=[RpcType.UNARY, RpcType.SERVER_STREAMING],
            method_names=["GetInfo", "StreamInfo"],
            request_dataclass=TestMessage,
            response_dataclass=AnotherMessage,
        )

        expected_service_definition = (
            "service TestService {\n"
            "  rpc GetInfo (TestMessage) returns (AnotherMessage);\n"
            "  rpc StreamInfo (TestMessage) returns (stream AnotherMessage);\n"
            "}\n"
        )

        service_definition = service.generate_service_definition()
        self.assertEqual(
            service_definition.strip(), expected_service_definition.strip()
        )


if __name__ == "__main__":
    unittest.main()
