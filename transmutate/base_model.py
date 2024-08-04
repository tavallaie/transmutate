from dataclasses import fields, MISSING
from typing import Type
import json


class BaseModel:
    def __post_init__(self):
        # Run validation methods
        self.run_validations()

    def run_validations(self):
        # Iterate over all fields and check for validation methods
        for field_name in self.__annotations__:
            validation_method_name = f"validation_{field_name}"
            if hasattr(self, validation_method_name):
                validation_method = getattr(self, validation_method_name)
                validation_method()

    def to_proto(self, directory: str = "."):
        from transmutate.proto_handler import (
            ProtoHandler,
        )  # Import here to avoid circular import

        proto_generator = ProtoHandler(self)
        proto_content = proto_generator.generate_proto()

        # Use the model's class name as the filename
        filename = f"{directory}/{self.__class__.__name__.lower()}.proto"

        # Write the Proto content to the file
        proto_generator.write_proto_file(filename)
        return proto_content

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_jsonb(self):
        return json.dumps(self.to_dict(), separators=(",", ":"))

    @classmethod
    def from_proto(cls: Type["BaseModel"], proto_data: str) -> "BaseModel":
        # Placeholder: Parse Proto data and create an instance of the dataclass
        # Requires a real parser for production code
        return cls.from_dict(json.loads(proto_data))  # Simulating using JSON parsing

    @classmethod
    def from_json(cls: Type["BaseModel"], json_data: str) -> "BaseModel":
        data_dict = json.loads(json_data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_jsonb(cls: Type["BaseModel"], jsonb_data: str) -> "BaseModel":
        data_dict = json.loads(jsonb_data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_dict(cls: Type["BaseModel"], data_dict: dict) -> "BaseModel":
        field_values = {}
        for field in fields(cls):
            field_name = field.name
            if field_name in data_dict:
                field_values[field_name] = data_dict[field_name]
            elif field.default is not MISSING:
                field_values[field_name] = field.default
            elif field.default_factory is not MISSING:
                field_values[field_name] = field.default_factory()
            else:
                raise ValueError(f"Missing required field '{field_name}'")
        return cls(**field_values)

    def to_dict(self) -> dict:
        return {field.name: getattr(self, field.name) for field in fields(self)}
