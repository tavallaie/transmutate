import json
from typing import Any


class JSONBHandler:
    def __init__(self, obj: Any):
        self.obj = obj

    def to_jsonb(self) -> str:
        data = self.serialize_obj(self.obj)
        return json.dumps(data, separators=(",", ":"))

    @staticmethod
    def parse_jsonb(jsonb_data: str) -> dict:
        return json.loads(jsonb_data)

    def serialize_obj(self, obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                result[key] = self.serialize_obj(value)
            return result
        elif isinstance(obj, list):
            return [self.serialize_obj(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.serialize_obj(value) for key, value in obj.items()}
        else:
            return obj
