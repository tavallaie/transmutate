import json as json_lib
from typing import Optional, List, Any
from dataclasses import asdict, fields
from .base import BaseModel


class SerializationMixin:
    def __init__(self, model):
        self.model = model

    def to_dict(self, fields: Optional[List[str]] = None) -> dict:
        """
        Convert the dataclass instance to a dictionary, optionally including only specified fields.

        :param fields: List of field names to include. If None, include all fields.
        :return: Dictionary representation of the instance.
        """
        all_fields = asdict(self.model)

        # Filter for specified fields
        if fields is not None:
            filtered_dict = {}
            for key in fields:
                value = all_fields.get(key)
                if hasattr(
                    value, "to_dict"
                ):  # Use hasattr instead of isinstance to check method existence
                    filtered_dict[key] = value.to_dict()  # Serialize nested BaseModel
                elif (
                    isinstance(value, list)
                    and len(value) > 0
                    and hasattr(value[0], "to_dict")
                ):
                    filtered_dict[key] = [
                        item.to_dict() for item in value
                    ]  # Serialize list of BaseModel
                else:
                    filtered_dict[key] = value
            return filtered_dict

        # Handle all fields
        for key, value in all_fields.items():
            if hasattr(
                value, "to_dict"
            ):  # Use hasattr instead of isinstance to check method existence
                all_fields[key] = value.to_dict()  # Serialize nested BaseModel
            elif (
                isinstance(value, list)
                and len(value) > 0
                and hasattr(value[0], "to_dict")
            ):
                all_fields[key] = [
                    item.to_dict() for item in value
                ]  # Serialize list of BaseModel
        return all_fields

    def to_json(self, fields: Optional[List[str]] = None) -> str:
        """
        Convert the dataclass instance to a JSON string, optionally including only specified fields.

        :param fields: List of field names to include. If None, include all fields.
        :return: JSON string representation of the instance.
        """
        return json_lib.dumps(self.to_dict(fields), indent=2)

    def to_jsonb(self, fields: Optional[List[str]] = None) -> bytes:
        """
        Convert the dataclass instance to a JSONB format (binary JSON), optionally including only specified fields.

        :param fields: List of field names to include. If None, include all fields.
        :return: JSONB bytes representation of the instance.
        """
        return json_lib.dumps(self.to_dict(fields)).encode("utf-8")

    @staticmethod
    def from_dict(data: dict) -> Any:
        """
        Create a dataclass instance from a dictionary.

        :param data: Dictionary containing the data.
        :return: An instance of the dataclass.
        """
        cls = SerializationMixin._find_class(data)
        field_types = {f.name: f.type for f in fields(cls)}

        for key, value in data.items():
            if key in field_types and hasattr(field_types[key], "from_dict"):
                data[key] = field_types[key].from_dict(value)
            elif (
                key in field_types
                and isinstance(field_types[key], list)
                and hasattr(field_types[key][0], "from_dict")
            ):
                data[key] = [field_types[key][0].from_dict(item) for item in value]

        return cls(**data)

    @staticmethod
    def from_json(json_str: str) -> Any:
        """
        Create a dataclass instance from a JSON string.

        :param json_str: JSON string containing the data.
        :return: An instance of the dataclass.
        """
        data = json_lib.loads(json_str)
        return SerializationMixin.from_dict(data)

    @staticmethod
    def _find_class(data: dict) -> Any:
        """
        Determine the class type for the given data.

        :param data: The data dictionary to analyze.
        :return: The class type that matches the data.
        """
        # Placeholder logic to determine the class; customize as needed
        # For demonstration, we'll assume it always returns BaseModel
        return BaseModel
