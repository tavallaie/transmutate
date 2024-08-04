import unittest
from dataclasses import dataclass, field
from enum import Enum

from typing import List, Optional
from transmutate.base_model.base import BaseModel
import os


class Gender(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2


@dataclass
class Address(BaseModel):
    street: str
    city: str
    zip_code: int

    def validation_zip_code(self, value):
        if not (10000 <= value <= 99999):
            raise ValueError("zip_code must be a five-digit number.")


@dataclass
class Company(BaseModel):
    name: str
    industry: str
    address: Address


@dataclass
class Person(BaseModel):
    name: str
    age: int
    gender: Gender
    email: Optional[str] = None
    addresses: List[Address] = field(default_factory=list)
    company: Optional[Company] = None

    def validation_name(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")

    def validation_age(self, value):
        if value < 0 or value > 120:
            raise ValueError("Age must be between 0 and 120.")


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.address1 = Address(street="123 Main St", city="Anytown", zip_code=12345)
        self.address2 = Address(street="456 Elm St", city="Othertown", zip_code=67890)
        self.company = Company(
            name="TechCorp", industry="Software", address=self.address1
        )
        self.person = Person(
            name="Alice",
            age=30,
            gender=Gender.FEMALE,
            addresses=[self.address1, self.address2],
            company=self.company,
        )

    def test_to_dict(self):
        expected_dict = {
            "name": "Alice",
            "age": 30,
            "gender": "Gender.FEMALE",
            "email": None,
            "addresses": [
                {"street": "123 Main St", "city": "Anytown", "zip_code": 12345},
                {"street": "456 Elm St", "city": "Othertown", "zip_code": 67890},
            ],
            "company": {
                "name": "TechCorp",
                "industry": "Software",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zip_code": 12345,
                },
            },
        }
        self.assertEqual(self.person.to_dict(), expected_dict)

    def test_to_json(self):
        expected_json = """{
  "name": "Alice",
  "age": 30,
  "gender": "Gender.FEMALE",
  "email": null,
  "addresses": [
    {
      "street": "123 Main St",
      "city": "Anytown",
      "zip_code": 12345
    },
    {
      "street": "456 Elm St",
      "city": "Othertown",
      "zip_code": 67890
    }
  ],
  "company": {
    "name": "TechCorp",
    "industry": "Software",
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "zip_code": 12345
    }
  }
}"""
        self.assertEqual(self.person.to_json(), expected_json)

    def test_to_jsonb(self):
        expected_jsonb = b'{"name": "Alice", "age": 30, "gender": "Gender.FEMALE", "email": null, "addresses": [{"street": "123 Main St", "city": "Anytown", "zip_code": 12345}, {"street": "456 Elm St", "city": "Othertown", "zip_code": 67890}], "company": {"name": "TechCorp", "industry": "Software", "address": {"street": "123 Main St", "city": "Anytown", "zip_code": 12345}}}'
        self.assertEqual(self.person.to_jsonb(), expected_jsonb)

    def test_from_dict(self):
        person_dict = {
            "name": "Alice",
            "age": 30,
            "gender": "Gender.FEMALE",
            "email": None,
            "addresses": [
                {"street": "123 Main St", "city": "Anytown", "zip_code": 12345},
                {"street": "456 Elm St", "city": "Othertown", "zip_code": 67890},
            ],
            "company": {
                "name": "TechCorp",
                "industry": "Software",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zip_code": 12345,
                },
            },
        }
        new_person = Person.from_dict(person_dict)
        self.assertEqual(new_person, self.person)

    def test_from_json(self):
        person_json = """{
            "name": "Alice",
            "age": 30,
            "gender": "Gender.FEMALE",
            "email": null,
            "addresses": [
                {"street": "123 Main St", "city": "Anytown", "zip_code": 12345},
                {"street": "456 Elm St", "city": "Othertown", "zip_code": 67890}
            ],
            "company": {
                "name": "TechCorp",
                "industry": "Software",
                "address": {"street": "123 Main St", "city": "Anytown", "zip_code": 12345}
            }
        }"""
        new_person = Person.from_json(person_json)
        self.assertEqual(new_person, self.person)

    def test_validation(self):
        with self.assertRaises(ValueError):
            Person(name="", age=150, gender=Gender.FEMALE)

        with self.assertRaises(ValueError):
            Address(
                street="123 Main St", city="Anytown", zip_code=999
            )  # Invalid zip code

    def test_proto_generation(self):
        # Generate ProtoBuf file and check its content
        self.person.to_proto(path_dir=".")
        proto_file_path = "./person.proto"
        self.assertTrue(os.path.exists(proto_file_path))

        # Check content of generated ProtoBuf file
        with open(proto_file_path, "r") as file:
            proto_content = file.read()

        expected_proto_content = """syntax = "proto3";
package default_package;

message Address {
    string street = 1;
    string city = 2;
    int32 zip_code = 3;
}

message Company {
    string name = 1;
    string industry = 2;
    Address address = 3;
}

message Person {
    string name = 1;
    int32 age = 2;
    Gender gender = 3;
    string email = 4;
    repeated Address addresses = 5;
    Company company = 6;
}

enum Gender {
    MALE = 0;
    FEMALE = 1;
    OTHER = 2;
}
"""
        self.assertEqual(proto_content.strip(), expected_proto_content.strip())

        # Clean up generated file
        os.remove(proto_file_path)


if __name__ == "__main__":
    unittest.main()
