from dataclasses import dataclass, field
from typing import List, Optional
from transmutate.base_model import BaseModel


@dataclass
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

    def validation_zip_code(self):
        if not self.zip_code.isdigit() or len(self.zip_code) != 5:
            raise ValueError("Zip code must be a 5-digit number.")


@dataclass
class Person(BaseModel):
    name: str
    age: int
    email: Optional[str] = None
    phone_numbers: List[str] = field(default_factory=list)

    def validation_age(self):
        if not (0 <= self.age <= 120):
            raise ValueError("Age must be between 0 and 120.")

    def validation_email(self):
        if self.email and "@" not in self.email:
            raise ValueError("Invalid email address.")
