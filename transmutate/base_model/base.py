from dataclasses import dataclass, field
from typing import List
from .serialization import SerializationMixin
from .protobuf import ProtoBufMixin
from .validation import ValidationMixin


@dataclass
class BaseModel(SerializationMixin, ProtoBufMixin, ValidationMixin):
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

    # Class attribute for custom imports and package name
    custom_imports: List[str] = field(default_factory=list, init=False)
    package_name: str = field(default="default_package", init=False)

    def __post_init__(self):
        """
        Custom validation logic after initialization.
        Override in subclasses for specific validation.
        Looks for validation_<fieldname> methods for dynamic field validation.
        """
        self.run_validations()
