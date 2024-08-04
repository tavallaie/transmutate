from dataclasses import is_dataclass
from typing import Type, Any, List, Optional


class ProtoHandler:
    def __init__(self, dataclass_obj):
        self.dataclass_obj = dataclass_obj
        self.proto_definitions = []  # Store all message definitions

    def generate_proto(self) -> str:
        # Start processing the root dataclass
        self.process_dataclass(self.dataclass_obj.__class__)

        # Join all message definitions into a single proto string
        proto_content = "\n".join(['syntax = "proto3";', ""] + self.proto_definitions)
        return proto_content

    def process_dataclass(self, dataclass_type, parent_names: List[str] = []) -> str:
        # Build a unique message name
        message_name = "_".join(parent_names + [dataclass_type.__name__])
        proto_lines = [f"message {message_name} {{"]

        fields = dataclass_type.__annotations__
        type_mapping = {
            int: "int32",
            float: "float",
            str: "string",
            bool: "bool",
            list: "repeated",
            dict: "map",
            # Add more types as needed
        }

        for index, (field_name, field_type) in enumerate(fields.items(), start=1):
            proto_type = self.get_proto_type(
                field_type, type_mapping, parent_names + [dataclass_type.__name__]
            )
            proto_lines.append(f"  {proto_type} {field_name} = {index};")

        proto_lines.append("}")
        self.proto_definitions.append(
            "\n".join(proto_lines)
        )  # Add this message to definitions

        return message_name

    def get_proto_type(self, field_type, type_mapping, parent_names):
        # Handle special types like lists and Optionals
        if hasattr(field_type, "__origin__"):
            origin = field_type.__origin__
            args = field_type.__args__
            if origin is list:
                inner_type = args[0]
                return f"{type_mapping[list]} {self.get_proto_type(inner_type, type_mapping, parent_names)}"
            elif origin is dict and len(args) == 2:
                return f"{type_mapping[dict]}<{self.get_proto_type(args[0], type_mapping, parent_names)}, {self.get_proto_type(args[1], type_mapping, parent_names)}>"
            elif origin is Optional:
                return self.get_proto_type(args[0], type_mapping, parent_names)

        # Handle nested dataclasses
        if is_dataclass(field_type):
            nested_message_name = self.process_dataclass(field_type, parent_names)
            return nested_message_name

        return type_mapping.get(field_type, "string")
