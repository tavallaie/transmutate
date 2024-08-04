from dataclasses import fields, MISSING, is_dataclass
from typing import Type, Any, List, Optional


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

    def to_proto(self):
        from transmutate.proto_handler import (
            ProtoHandler,
        )  # Import here to avoid circular import

        proto_generator = ProtoHandler(self)
        return proto_generator.generate_proto()

    def to_json(self):
        from transmutate.json_handler import (
            JSONHandler,
        )  # Import here to avoid circular import

        json_handler = JSONHandler(self)
        return json_handler.to_json()

    def to_jsonb(self):
        from transmutate.jsonb_handler import (
            JSONBHandler,
        )  # Import here to avoid circular import

        jsonb_handler = JSONBHandler(self)
        return jsonb_handler.to_jsonb()

    @classmethod
    def from_proto(cls: Type["BaseModel"], proto_data: str) -> "BaseModel":
        # Placeholder: Parse Proto data and create an instance of the dataclass
        # Requires a real parser for production code
        from transmutate.json_handler import (
            JSONHandler,
        )  # Import here to avoid circular import

        parsed_data = JSONHandler.parse_json(
            proto_data
        )  # Simulating using JSON parsing
        return cls.from_dict(parsed_data)

    @classmethod
    def from_json(cls: Type["BaseModel"], json_data: str) -> "BaseModel":
        from transmutate.json_handler import (
            JSONHandler,
        )  # Import here to avoid circular import

        data_dict = JSONHandler.parse_json(json_data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_jsonb(cls: Type["BaseModel"], jsonb_data: str) -> "BaseModel":
        from transmutate.jsonb_handler import (
            JSONBHandler,
        )  # Import here to avoid circular import

        data_dict = JSONBHandler.parse_jsonb(jsonb_data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_dict(cls: Type["BaseModel"], data_dict: dict) -> "BaseModel":
        # Create an instance from a dictionary, assuming no nested dataclasses
        return cls(**data_dict)
