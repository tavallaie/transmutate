import os
import subprocess
import logging
from typing import Optional, List, Any, Type, Union
from dataclasses import MISSING
from enum import Enum
from .base import BaseModel  # Import BaseModel to avoid undefined errors

# Configure logging
logging.basicConfig(level=logging.INFO)


class ProtoBufMixin:
    @classmethod
    def to_proto(cls, path_dir: str = ".", fields: Optional[List[str]] = None):
        """
        Generate a ProtoBuf file for the model and optionally compile it, including specific fields if specified.

        :param path_dir: Directory where the .proto file will be saved.
        :param fields: List of field names to include. If None, include all fields.
        :default: Current directory (".")
        """
        logging.info(f"Generating ProtoBuf for {cls.__name__}...")

        # Ensure the directory exists
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
            logging.info(f"Created directory: {path_dir}")

        # Generate ProtoBuf message and write to file
        proto_content = cls.generate_proto_message(fields)
        proto_file_path = os.path.join(path_dir, f"{cls.__name__.lower()}.proto")

        try:
            with open(proto_file_path, "w") as file:
                file.write(proto_content)
            logging.info(f"Proto file generated at {proto_file_path}")

            # Automatically compile ProtoBuf file
            cls.compile_proto(proto_file_path, path_dir)

        except Exception as e:
            logging.error(f"Failed to write ProtoBuf file: {e}")

    @classmethod
    def generate_proto_message(cls, fields: Optional[List[str]] = None) -> str:
        """
        Generate ProtoBuf message definition for the class, including nested messages and enums.

        :param fields: List of field names to include. If None, include all fields.
        :return: A string representation of the ProtoBuf message.
        """
        header = cls.generate_proto_file_header()
        message = f"message {cls.__name__} {{\n"

        for idx, field_info in enumerate(fields(cls), start=1):
            if fields and field_info.name not in fields:
                continue

            name = field_info.metadata.get("proto_name", field_info.name)
            typ = field_info.type

            # Handle nested messages and enums
            if isinstance(typ, type) and issubclass(typ, BaseModel):
                nested_message = typ.generate_proto_message().strip()
                message += f"    {nested_message.replace('\n', '\n    ')}\n"
                proto_type = typ.__name__
            elif isinstance(typ, type) and issubclass(typ, Enum):
                enum_def = cls.generate_enum_definition(typ).strip()
                message += f"    {enum_def.replace('\n', '\n    ')}\n"
                proto_type = typ.__name__
            else:
                proto_type = cls.get_proto_type(typ)

            # Handling default values and options
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

    @classmethod
    def get_proto_type(cls, python_type: Any) -> str:
        """
        Determine the ProtoBuf type from a Python type.

        :param python_type: The Python type to be converted.
        :return: Corresponding ProtoBuf type.
        """
        if hasattr(python_type, "__origin__"):
            if python_type.__origin__ is list:
                inner_type = python_type.__args__[0]
                proto_type = cls.python_to_proto_type.get(
                    inner_type, inner_type.__name__
                )
                return f"repeated {proto_type}"
            elif python_type.__origin__ is Union and type(None) in python_type.__args__:
                inner_type = next(
                    arg for arg in python_type.__args__ if arg is not type(None)
                )
                return cls.python_to_proto_type.get(inner_type, inner_type.__name__)
        elif isinstance(python_type, type) and issubclass(python_type, Enum):
            return python_type.__name__
        else:
            return cls.python_to_proto_type.get(python_type, python_type.__name__)

    @classmethod
    def generate_enum_definition(cls, enum_type: Type[Enum]) -> str:
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

    @classmethod
    def generate_proto_file_header(cls) -> str:
        """
        Generate ProtoBuf file header including syntax, package, and custom imports.

        :return: ProtoBuf file header as a string.
        """
        header = 'syntax = "proto3";\n'
        header += f"package {cls.package_name};\n\n"
        for imp in cls.custom_imports:
            header += f'import "{imp}";\n'
        header += "\n"
        return header

    @classmethod
    def compile_proto(cls, proto_file_path: str, output_dir: str):
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
