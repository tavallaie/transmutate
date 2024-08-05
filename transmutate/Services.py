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
