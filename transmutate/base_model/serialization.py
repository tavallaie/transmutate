import json as json_lib
from typing import Optional, List, Type, get_type_hints
from .base import BaseModel  # Import BaseModel to avoid undefined errors
from dataclasses import asdict


class SerializationMixin:
    def to_dict(self, fields: Optional[List[str]] = None) -> dict:
        """
        Convert the dataclass instance to a dictionary, optionally including only specified fields.

        :param fields: List of field names to include. If None, include all fields.
        :return: Dictionary representation of the instance.
        """
        all_fields = asdict(self)

        # Filter for specified fields
        if fields is not None:
            filtered_dict = {}
            for key in fields:
                value = all_fields.get(key)
                if isinstance(value, BaseModel):
                    filtered_dict[key] = value.to_dict(
                        fields
                    )  # Serialize nested BaseModel
                elif (
                    isinstance(value, list)
                    and len(value) > 0
                    and isinstance(value[0], BaseModel)
                ):
                    filtered_dict[key] = [
                        item.to_dict(fields) for item in value
                    ]  # Serialize list of BaseModel
                else:
                    filtered_dict[key] = value
            return filtered_dict

        # Handle all fields
        for key, value in all_fields.items():
            if isinstance(value, BaseModel):
                all_fields[key] = value.to_dict()  # Serialize nested BaseModel
            elif (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], BaseModel)
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
    def from_dict(data: dict) -> "BaseModel":
        """
        Create a dataclass instance from a dictionary.

        :param data: Dictionary containing the data.
        :return: An instance of the dataclass.
        """
        cls = BaseModel._find_class(data)
        field_types = get_type_hints(cls)
        for key, value in data.items():
            if isinstance(field_types.get(key), type) and issubclass(
                field_types[key], BaseModel
            ):
                data[key] = field_types[key].from_dict(value)
            elif isinstance(field_types.get(key), list) and issubclass(
                field_types[key].__args__[0], BaseModel
            ):
                data[key] = [
                    field_types[key].__args__[0].from_dict(item) for item in value
                ]
        return cls(**data)

    @staticmethod
    def from_json(json_str: str) -> "BaseModel":
        """
        Create a dataclass instance from a JSON string.

        :param json_str: JSON string containing the data.
        :return: An instance of the dataclass.
        """
        data = json_lib.loads(json_str)
        return BaseModel.from_dict(data)

    @staticmethod
    def _find_class(data: dict) -> Type:
        """
        Find the class type for the given data based on key indicators.

        :param data: The data dictionary to analyze.
        :return: The class type that matches the data.
        """
        # This is a placeholder implementation; you need a mechanism to determine the class type
        # For now, it assumes all instances are of BaseModel, replace this logic with your own
        return BaseModel
