from dataclasses import dataclass, field, fields, MISSING, asdict
from typing import List, Any, Optional, Type, Union
import json as json_lib
import os
import subprocess
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)


class SerializationHandler:
    @staticmethod
    def to_dict(model: Any, field_names: Optional[List[str]] = None) -> dict:
        """
        Convert the dataclass instance to a dictionary, optionally including only specified fields.
        """
        all_fields = asdict(model)

        if field_names is not None:
            filtered_dict = {}
            for key in field_names:
                value = all_fields.get(key)
                if hasattr(value, "to_dict"):
                    filtered_dict[key] = value.to_dict()
                elif (
                    isinstance(value, list)
                    and len(value) > 0
                    and hasattr(value[0], "to_dict")
                ):
                    filtered_dict[key] = [item.to_dict() for item in value]
                else:
                    filtered_dict[key] = value
            return filtered_dict

        for key, value in all_fields.items():
            if hasattr(value, "to_dict"):
                all_fields[key] = value.to_dict()
            elif (
                isinstance(value, list)
                and len(value) > 0
                and hasattr(value[0], "to_dict")
            ):
                all_fields[key] = [item.to_dict() for item in value]

        return all_fields

    @staticmethod
    def to_json(model: Any, field_names: Optional[List[str]] = None) -> str:
        """
        Convert the dataclass instance to a JSON string, optionally including only specified fields.
        """
        return json_lib.dumps(
            SerializationHandler.to_dict(model, field_names), indent=2
        )

    @staticmethod
    def to_jsonb(model: Any, field_names: Optional[List[str]] = None) -> bytes:
        """
        Convert the dataclass instance to a JSONB format (binary JSON), optionally including only specified fields.
        """
        return json_lib.dumps(SerializationHandler.to_dict(model, field_names)).encode(
            "utf-8"
        )

    @staticmethod
    def from_dict(data: dict, cls: Type) -> Any:
        """
        Create a dataclass instance from a dictionary, ignoring fields not present in the dataclass.
        """
        # Filter out fields that are not part of the dataclass
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        # Handle nested BaseModel instances
        field_types = {f.name: f.type for f in fields(cls)}
        for key, value in filtered_data.items():
            field_type = field_types.get(key)

            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                filtered_data[key] = field_type.from_dict(value)
            elif (
                isinstance(field_type, list)
                and len(field_type) > 0
                and issubclass(field_type[0], BaseModel)
            ):
                filtered_data[key] = [field_type[0].from_dict(item) for item in value]

        return cls(**filtered_data)

    @staticmethod
    def from_json(json_str: str, cls: Type) -> Any:
        """
        Create a dataclass instance from a JSON string, ignoring fields not present in the dataclass.
        """
        data = json_lib.loads(json_str)
        return SerializationHandler.from_dict(data, cls)


class ProtoBufHandler:
    @staticmethod
    def to_proto(
        model: Any, path_dir: str = ".", field_names: Optional[List[str]] = None
    ):
        """
        Generate a ProtoBuf file for the model and optionally compile it, including specific fields if specified.

        :param model: The model instance to be converted to ProtoBuf.
        :param path_dir: Directory where the .proto file will be saved.
        :param field_names: List of field names to include. If None, include all fields.
        :default: Current directory (".")
        """
        logging.info(f"Generating ProtoBuf for {model.__class__.__name__}...")

        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
            logging.info(f"Created directory: {path_dir}")

        proto_content = ProtoBufHandler.generate_proto_message(model, field_names)
        proto_file_path = os.path.join(
            path_dir, f"{model.__class__.__name__.lower()}.proto"
        )

        try:
            with open(proto_file_path, "w") as file:
                file.write(proto_content)
            logging.info(f"Proto file generated at {proto_file_path}")

            ProtoBufHandler.compile_proto(proto_file_path, path_dir)

        except Exception as e:
            logging.error(f"Failed to write ProtoBuf file: {e}")

    @staticmethod
    def generate_proto_message(
        model: Any, field_names: Optional[List[str]] = None
    ) -> str:
        """
        Generate ProtoBuf message definition for the class, including nested messages and enums.

        :param model: The model instance to generate a ProtoBuf message for.
        :param field_names: List of field names to include. If None, include all fields.
        :return: A string representation of the ProtoBuf message.
        """
        header = ProtoBufHandler.generate_proto_file_header(model)
        message = f"message {model.__class__.__name__} {{\n"

        for idx, field_info in enumerate(fields(model), start=1):
            if field_names and field_info.name not in field_names:
                continue

            name = field_info.metadata.get("proto_name", field_info.name)
            typ = field_info.type

            if isinstance(typ, type) and issubclass(typ, BaseModel):
                nested_message = ProtoBufHandler.generate_proto_message(
                    typ, field_names
                ).strip()
                indented_nested_message = nested_message.replace("\n", "\n    ")
                message += f"    {indented_nested_message}\n"
                proto_type = typ.__name__
            elif isinstance(typ, type) and issubclass(typ, Enum):
                enum_def = ProtoBufHandler.generate_enum_definition(typ).strip()
                indented_enum_def = enum_def.replace("\n", "\n    ")
                message += f"    {indented_enum_def}\n"
                proto_type = typ.__name__
            else:
                proto_type = ProtoBufHandler.get_proto_type(model, typ)

            options = ""
            if field_info.default is not MISSING:
                default_value = field_info.default
                if isinstance(default_value, str):
                    options = f'[default = "{default_value}"]'
                elif isinstance(default_value, (int, float, bool)):
                    options = f"[default = {default_value}]"

            message += f"    {proto_type} {name} = {idx} {options};\n"

        message += "}\n\n"
        return header + message

    @staticmethod
    def get_proto_type(model: Any, python_type: Any) -> str:
        """
        Determine the ProtoBuf type from a Python type.

        :param model: The model instance to get the ProtoBuf type for.
        :param python_type: The Python type to be converted.
        :return: Corresponding ProtoBuf type.
        """
        python_to_proto_type = {
            str: "string",
            int: "int32",
            float: "float",
            bool: "bool",
            bytes: "bytes",
            list: "repeated",
        }

        if hasattr(python_type, "__origin__"):
            if python_type.__origin__ is list:
                inner_type = python_type.__args__[0]
                proto_type = python_to_proto_type.get(inner_type, inner_type.__name__)
                return f"repeated {proto_type}"
            elif python_type.__origin__ is Union and type(None) in python_type.__args__:
                inner_type = next(
                    arg for arg in python_type.__args__ if arg is not type(None)
                )
                return python_to_proto_type.get(inner_type, inner_type.__name__)
        elif isinstance(python_type, type) and issubclass(python_type, Enum):
            return python_type.__name__
        else:
            return python_to_proto_type.get(python_type, python_type.__name__)

    @staticmethod
    def generate_enum_definition(enum_type: Type[Enum]) -> str:
        """
        Generate ProtoBuf enum definition for a Python Enum class.

        :param enum_type: The Enum class.
        :return: ProtoBuf enum definition as a string.
        """
        enum_def = f"enum {enum_type.__name__} {{\n"
        for name, member in enum_type.__members__.items():
            enum_def += f"    {name} = {member.value};\n"
        enum_def += "}\n"
        return enum_def

    @staticmethod
    def generate_proto_file_header(model: Any) -> str:
        """
        Generate ProtoBuf file header including syntax, package, and custom imports.

        :param model: The model instance to generate a ProtoBuf header for.
        :return: ProtoBuf file header as a string.
        """
        header = f'syntax = "proto3";\n'
        header += f"package {model.package_name};\n\n"
        for imp in model.custom_imports:
            header += f'import "{imp}";\n'
        header += "\n"
        return header

    @staticmethod
    def compile_proto(proto_file_path: str, output_dir: str):
        """
        Compile the ProtoBuf file to generate Python classes.

        :param proto_file_path: Path to the ProtoBuf file.
        :param output_dir: Directory for the generated Python files.
        """
        try:
            subprocess.run(
                ["protoc", "--python_out", output_dir, proto_file_path], check=True
            )
            logging.info(f"Compiled ProtoBuf file: {proto_file_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error compiling ProtoBuf file: {e}")


class ValidationHandler:
    @staticmethod
    def run_validations(model: Any):
        """
        Runs all dynamic validations on the instance's fields.
        """
        for field_info in fields(model):
            validation_method_name = f"validation_{field_info.name}"
            validation_method = getattr(model, validation_method_name, None)
            if callable(validation_method):
                validation_method(getattr(model, field_info.name))


@dataclass
class BaseModel:
    """
    Base class for models that need to be serialized into multiple formats.
    Provides serialization to dict, JSON, and JSONB formats, and handles
    ProtoBuf file generation and compilation. Supports dynamic field validation.
    """

    # Class attribute for custom imports and package name
    custom_imports: List[str] = field(default_factory=list, init=False)
    package_name: str = field(default="default_package", init=False)

    # Inject handlers as default properties
    serialization_handler: SerializationHandler = field(
        default_factory=SerializationHandler, init=False, repr=False
    )
    protobuf_handler: ProtoBufHandler = field(
        default_factory=ProtoBufHandler, init=False, repr=False
    )
    validation_handler: ValidationHandler = field(
        default_factory=ValidationHandler, init=False, repr=False
    )

    def __post_init__(self):
        """
        Custom validation logic after initialization.
        Override in subclasses for specific validation.
        Looks for validation_<fieldname> methods for dynamic field validation.
        """
        self.run_validations()

    def to_dict(self, field_names: List[str] = None) -> dict:
        return self.serialization_handler.to_dict(self, field_names)

    def to_json(self, field_names: List[str] = None) -> str:
        return self.serialization_handler.to_json(self, field_names)

    def to_jsonb(self, field_names: List[str] = None) -> bytes:
        return self.serialization_handler.to_jsonb(self, field_names)

    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        return SerializationHandler.from_dict(data, cls)

    @classmethod
    def from_json(cls, json_str: str) -> "BaseModel":
        return SerializationHandler.from_json(json_str, cls)

    def to_proto(self, path_dir: str = ".", field_names: Optional[List[str]] = None):
        self.protobuf_handler.to_proto(self, path_dir, field_names)

    def run_validations(self):
        self.validation_handler.run_validations(self)
