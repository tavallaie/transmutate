from dataclasses import dataclass, field
from typing import List, Type


@dataclass
class BaseModel:
    """
    Base class for models that need to be serialized into multiple formats.
    Provides serialization to dict, JSON, and JSONB formats, and handles
    ProtoBuf file generation and compilation. Supports dynamic field validation.
    """

    # Mapping of Python types to ProtoBuf types
    python_to_proto_type = {
        str: "string",  # String mapping
        int: "int32",  # 32-bit integer
        float: "float",  # Floating point
        bool: "bool",  # Boolean type
        bytes: "bytes",  # Byte array
        list: "repeated",  # Repeated field (for lists)
    }

    custom_imports: List[str] = field(default_factory=list, init=False)
    package_name: str = field(default="default_package", init=False)

    def __post_init__(self):
        """
        Custom validation logic after initialization.
        Override in subclasses for specific validation.
        Looks for validation_<fieldname> methods for dynamic field validation.
        """
        self.run_validations()

    def inject_serialization_mixin(self, serialization_mixin: Type):
        self.serialization_mixin = serialization_mixin(self)

    def inject_protobuf_mixin(self, protobuf_mixin: Type):
        self.protobuf_mixin = protobuf_mixin(self)

    def inject_validation_mixin(self, validation_mixin: Type):
        self.validation_mixin = validation_mixin(self)

    def to_dict(self, fields: List[str] = None) -> dict:
        return self.serialization_mixin.to_dict(fields)

    def to_json(self, fields: List[str] = None) -> str:
        return self.serialization_mixin.to_json(fields)

    def to_jsonb(self, fields: List[str] = None) -> bytes:
        return self.serialization_mixin.to_jsonb(fields)

    def to_proto(self, path_dir: str = ".", fields: List[str] = None):
        self.protobuf_mixin.to_proto(path_dir, fields)

    def run_validations(self):
        self.validation_mixin.run_validations()
