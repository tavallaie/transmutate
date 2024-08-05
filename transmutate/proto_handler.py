from typing import Optional


class ProtoHandler:
    def __init__(self, dataclass_obj):
        self.dataclass_obj = dataclass_obj
        self.proto_definitions = []  # Store all message definitions

    def generate_proto(self) -> str:
        # Clear any previous definitions to prevent duplicates
        self.proto_definitions.clear()

        return self.process_dataclass(self.dataclass_obj.__class__)

    def process_dataclass(self, dataclass_type) -> str:
        # Build a message name
        message_name = dataclass_type.__name__
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
            proto_type = self.get_proto_type(field_type, type_mapping)
            proto_lines.append(f"  {proto_type} {field_name} = {index};")

        proto_lines.append("}")
        self.proto_definitions.append(
            "\n".join(proto_lines)
        )  # Add this message to definitions

        return message_name

    def get_proto_type(self, field_type, type_mapping):
        # Handle lists and Optionals
        if hasattr(field_type, "__origin__"):
            origin = field_type.__origin__
            args = field_type.__args__
            if origin is list:
                inner_type = args[0]
                return f"{type_mapping[list]} {self.get_proto_type(inner_type, type_mapping)}"
            elif origin is Optional:
                return self.get_proto_type(args[0], type_mapping)

        return type_mapping.get(field_type, "string")
