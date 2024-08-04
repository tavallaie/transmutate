import json
from dataclasses import fields, is_dataclass
from typing import Any


class JSONHandler:
    def __init__(self, dataclass_obj):
        self.dataclass_obj = dataclass_obj

    def to_json(self) -> str:
        data = self.serialize_dataclass(self.dataclass_obj)
        return json.dumps(data, indent=4)

    @staticmethod
    def parse_json(json_data: str) -> dict:
        return json.loads(json_data)

    def serialize_dataclass(self, obj: Any) -> Any:
        if is_dataclass(obj):
            result = {}
            for field in fields(obj):
                value = getattr(obj, field.name)
                result[field.name] = self.serialize_dataclass(value)
            return result
        elif isinstance(obj, list):
            return [self.serialize_dataclass(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.serialize_dataclass(value) for key, value in obj.items()}
        else:
            return obj