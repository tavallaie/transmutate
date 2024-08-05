import unittest
import os
from transmutate import Service, RpcType
from transmutate import BaseModel, ProtoGenerator
from typing import List


class TestMessage(BaseModel):
    name: str
    age: int
    email: str
    phone_numbers: List[str]


class AnotherMessage(BaseModel):
    status: str
    message: str


class TestProtoGenerator(unittest.TestCase):
    def setUp(self):
        self.services = [
            Service(
                name="TestService",
                types=[RpcType.UNARY, RpcType.SERVER_STREAMING],
                method_names=["GetInfo", "StreamInfo"],
                request_dataclass=TestMessage,
                response_dataclass=AnotherMessage,
            )
        ]
        self.generator = ProtoGenerator(
            service_name="TestService", services=self.services
        )

    def test_generate_header(self):
        expected_header = """
syntax = "proto3";

package testservice;

// TestService service definition
"""
        header = self.generator._generate_header()
        self.assertEqual(header.strip(), expected_header.strip())

    def test_generate_service(self):
        expected_service_content = """
service TestService {
  rpc GetInfo (TestMessage) returns (AnotherMessage);
  rpc StreamInfo (TestMessage) returns (stream AnotherMessage);
}

"""
        service_content = self.generator._generate_service()
        self.assertEqual(service_content.strip(), expected_service_content.strip())

    def test_generate_messages(self):
        expected_messages_content = """
// Request and response messages
message TestMessage {
  string name = 1;
  int32 age = 2;
  string email = 3;
  repeated string phone_numbers = 4;
}

message AnotherMessage {
  string status = 1;
  string message = 2;
}
"""
        messages_content = self.generator._generate_messages()
        self.assertEqual(messages_content.strip(), expected_messages_content.strip())

    def test_write_proto_file(self):
        self.generator.generate_proto()
        self.assertTrue(os.path.exists(self.generator.proto_file_path))
        with open(self.generator.proto_file_path, "r") as proto_file:
            content = proto_file.read()
            expected_content = """
syntax = "proto3";

package testservice;

// TestService service definition

service TestService {
  rpc GetInfo (TestMessage) returns (AnotherMessage);
  rpc StreamInfo (TestMessage) returns (stream AnotherMessage);
}

// Request and response messages
message TestMessage {
  string name = 1;
  int32 age = 2;
  string email = 3;
  repeated string phone_numbers = 4;
}

message AnotherMessage {
  string status = 1;
  string message = 2;
}
"""
            self.assertEqual(content.strip(), expected_content.strip())
        os.remove(self.generator.proto_file_path)


if __name__ == "__main__":
    unittest.main()
