from typing import Type
import json


class BaseModel:
    def __init__(self, **kwargs):
        # Automatically set attributes for any keyword arguments passed
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        )  # Lazy import to avoid circular import

        proto_generator = ProtoHandler(self)
        return proto_generator.generate_proto()

    def to_json(self):
        from transmutate.json_handler import (
            JSONHandler,
        )  # Lazy import to avoid circular import

        json_handler = JSONHandler(self)
        return json_handler.to_json()

    def to_jsonb(self):
        from transmutate.jsonb_handler import (
            JSONBHandler,
        )  # Lazy import to avoid circular import

        jsonb_handler = JSONBHandler(self)
        return jsonb_handler.to_jsonb()

    @classmethod
    def from_proto(cls: Type["BaseModel"], proto_data: str) -> "BaseModel":
        # Placeholder: Parse Proto data and create an instance of the dataclass
        # Requires a real parser for production code
        return cls.from_dict(json.loads(proto_data))  # Simulating using JSON parsing

    @classmethod
    def from_json(cls: Type["BaseModel"], json_data: str) -> "BaseModel":
        from transmutate.json_handler import (
            JSONHandler,
        )  # Lazy import to avoid circular import

        data_dict = JSONHandler.parse_json(json_data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_jsonb(cls: Type["BaseModel"], jsonb_data: str) -> "BaseModel":
        from transmutate.jsonb_handler import (
            JSONBHandler,
        )  # Lazy import to avoid circular import

        data_dict = JSONBHandler.parse_jsonb(jsonb_data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_dict(cls, data_dict: dict) -> "BaseModel":
        # Initialize the fields directly from the data dictionary
        field_values = {}
        for (
            key,
            value,
        ) in cls.__annotations__.items():  # Assuming type hints are provided
            if key in data_dict:
                field_values[key] = data_dict[key]
            else:
                raise ValueError(f"Missing required field '{key}'")
        return cls(**field_values)

    def to_dict(self) -> dict:
        """Convert the model instance to a dictionary."""
        return self.__dict__.copy()

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"
