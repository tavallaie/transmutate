from dataclasses import dataclass, fields, is_dataclass, MISSING
from typing import List, Dict, Type, Any, get_origin, get_args


@dataclass
class Address:
    street: str
    city: str
    zip_code: str

    @classmethod
    def from_dict(cls: Type["Address"], data_dict: Dict[str, Any]) -> "Address":
        # Create an Address instance from a dictionary
        field_values = {}
        for field in fields(cls):
            field_name = field.name
            if field_name in data_dict:
                field_values[field_name] = data_dict[field_name]
            elif field.default is not MISSING:
                field_values[field_name] = field.default
            elif field.default_factory is not MISSING:
                field_values[field_name] = field.default_factory()
            else:
                raise ValueError(f"Missing required field '{field_name}'")
        return cls(**field_values)

    def to_dict(self) -> dict:
        # Convert Address instance to dictionary
        return {field.name: getattr(self, field.name) for field in fields(self)}


@dataclass
class Person:
    name: str
    age: int
    email: str
    phone_numbers: List[str]
    address: Address

    @classmethod
    def from_dict(cls: Type["Person"], data_dict: Dict[str, Any]) -> "Person":
        # Helper method to construct an instance from a dictionary
        field_values = {}
        for field in fields(cls):
            field_name = field.name
            field_type = field.type

            if field_name in data_dict:
                value = data_dict[field_name]

                # Debugging information
                print(
                    f"Processing field: {field_name}, Value: {value}, Field Type: {field_type}"
                )

                # Check if the field_type is a dataclass and value is a dictionary
                if is_dataclass(field_type) and isinstance(value, dict):
                    field_values[field_name] = field_type.from_dict(value)

                # Check if the field_type is a List and handle accordingly
                elif get_origin(field_type) is list:
                    inner_type = get_args(field_type)[0]
                    if is_dataclass(inner_type):
                        field_values[field_name] = [
                            inner_type.from_dict(item)
                            if isinstance(item, dict)
                            else item
                            for item in value
                        ]
                    else:
                        field_values[field_name] = value

                # Check if the field_type is a Dict and handle accordingly
                elif get_origin(field_type) is dict:
                    key_type, val_type = get_args(field_type)
                    if is_dataclass(val_type):
                        field_values[field_name] = {
                            k: val_type.from_dict(v) if isinstance(v, dict) else v
                            for k, v in value.items()
                        }
                    else:
                        field_values[field_name] = value

                # Handle other types directly
                else:
                    field_values[field_name] = value

            elif field.default is not MISSING:
                field_values[field_name] = field.default
            elif field.default_factory is not MISSING:
                field_values[field_name] = field.default_factory()
            else:
                raise ValueError(f"Missing required field '{field_name}'")

        return cls(**field_values)

    def to_dict(self) -> dict:
        # Convert the dataclass to a dictionary
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if is_dataclass(value):
                result[field.name] = value.to_dict()
            elif isinstance(value, list):
                # Convert lists of dataclasses to lists of dictionaries
                result[field.name] = [
                    item.to_dict() if is_dataclass(item) else item for item in value
                ]
            elif isinstance(value, dict):
                # Convert dictionaries with dataclass values to dictionaries of dictionaries
                result[field.name] = {
                    k: v.to_dict() if is_dataclass(v) else v for k, v in value.items()
                }
            else:
                result[field.name] = value
        return result


# Sample dictionary representing a Person
person_data = {
    "name": "Alice",
    "age": 28,
    "email": "alice@example.com",
    "phone_numbers": ["123-456-7890", "987-654-3210"],
    "address": {"street": "123 Maple St", "city": "Newtown", "zip_code": "54321"},
}

# Instantiate the Person dataclass from the dictionary
person_instance = Person.from_dict(person_data)

# Debug output
print("\nConstructed Person Instance:")
print(person_instance)
print("\nConverted back to dictionary:")
print(person_instance.to_dict())
