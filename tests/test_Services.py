# tests/test_Services.py

import unittest
from transmutate import BaseModel, Service, RpcType
from typing import List


class TestMessage(BaseModel):
    name: str
    age: int
    email: str
    phone_numbers: List[str]


class AnotherMessage(BaseModel):
    status: str
    message: str


class TestService(unittest.TestCase):
    def test_Service_creation(self):
        Service = Service(
            name="TestService",
            types=[RpcType.UNARY, RpcType.SERVER_STREAMING],
            request_dataclass=TestMessage,
            response_dataclass=AnotherMessage,
        )
        self.assertEqual(Service.name, "TestService")
        self.assertEqual(Service.types, [RpcType.UNARY, RpcType.SERVER_STREAMING])
        self.assertEqual(Service.request_dataclass, TestMessage)
        self.assertEqual(Service.response_dataclass, AnotherMessage)

    def test_request_message_generation(self):
        Service = Service(
            name="TestService", types=[RpcType.UNARY], request_dataclass=TestMessage
        )
        proto_message = Service.get_request_message()
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
        Service = Service(
            name="TestService", types=[RpcType.UNARY], response_dataclass=AnotherMessage
        )
        proto_message = Service.get_response_message()
        expected_message = (
            "message AnotherMessage {\n"
            "  string status = 1;\n"
            "  string message = 2;\n"
            "}\n"
        )
        self.assertEqual(proto_message.strip(), expected_message.strip())


if __name__ == "__main__":
    unittest.main()
