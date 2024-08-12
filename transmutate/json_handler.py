import json
from typing import Any


class JSONHandler:
    def __init__(self, obj):
        self.obj = obj

    def to_json(self) -> str:
        data = self.serialize_obj(self.obj)
        return json.dumps(data, indent=4)

    @staticmethod
    def parse_json(json_data: str) -> dict:
        return json.loads(json_data)

    def serialize_obj(self, obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            # This is an object that has a __dict__ attribute (like BaseModel or similar)
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
