from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Type


# Define the RpcType enum with method signature templates
class RpcType(Enum):
    UNARY = "  rpc {method_name} ({request_message}) returns ({response_message});\n"
    SERVER_STREAMING = (
        "  rpc {method_name} ({request_message}) returns (stream {response_message});\n"
    )
    CLIENT_STREAMING = (
        "  rpc {method_name} (stream {request_message}) returns ({response_message});\n"
    )
    BIDIRECTIONAL = "  rpc {method_name} (stream {request_message}) returns (stream {response_message});\n"


# Service dataclass
@dataclass
class Service:
    name: str
    types: List[RpcType]  # List of RpcType enums for the service
    method_names: List[str]  # List of method names corresponding to RpcTypes
    request_dataclass: Optional[Type] = None  # Optional dataclass for request
    response_dataclass: Optional[Type] = None  # Optional dataclass for response

    def get_request_message(self) -> str:
        """Generates the request message definition using to_proto."""
        if self.request_dataclass:
            return self.request_dataclass.to_proto()
        return ""

    def get_response_message(self) -> str:
        """Generates the response message definition using to_proto."""
        if self.response_dataclass:
            return self.response_dataclass.to_proto()
        return ""

    def generate_service_definition(self) -> str:
        """Generates the complete service definition including RPC methods."""
        service_definition = [f"service {self.name} {{\n"]
        request_message_name = (
            self.request_dataclass.__name__ if self.request_dataclass else "Empty"
        )
        response_message_name = (
            self.response_dataclass.__name__ if self.response_dataclass else "Empty"
        )

        for rpc_type, method_name in zip(self.types, self.method_names):
            rpc_method = rpc_type.value.format(
                method_name=method_name,
                request_message=request_message_name,
                response_message=response_message_name,
            )
            service_definition.append(rpc_method)

        service_definition.append("}\n")
        return "".join(service_definition)


# Define an Empty message for cases without specific request/response dataclasses
@dataclass
class Empty:
    pass

    @staticmethod
    def to_proto():
        return "message Empty {}\n"
