[![DOI](https://zenodo.org/badge/837882085.svg)](https://zenodo.org/doi/10.5281/zenodo.13226541)
# Transmutate

 Transmutate is a Python library designed to handle dataclass serialization and deserialization across various formats such as JSON, JSONB, and Protocol Buffers (Proto). The library supports both conversion to these formats and validation of dataclass fields.

 ## Features

 - **JSON Serialization**: Convert dataclasses to and from JSON format.
 - **JSONB Serialization**: Convert dataclasses to and from JSONB format, a compact version of JSON.
 - **Protocol Buffers Serialization**: Generate Proto definitions from dataclasses.
 - **Field Validation**: Custom validation for dataclass fields using `validation_<field>` methods.
 - **Service Definitions**: Define gRPC services with customizable RPC methods.
 - **Proto Generator**: Automatically generate Proto files including service and message definitions.
 - **Easy Integration**: Built on top of Python's dataclasses, allowing seamless integration with existing codebases.

 ## Installation

 You can install Transmutate via Poetry by adding it to your `pyproject.toml` file or by using the following command:

 ```bash
 poetry add transmutate
 ```

 Alternatively, if you're using pip, you can install it with:

 ```bash
 pip install transmutate
 ```

 ## Usage

 Below are some examples demonstrating how to use Transmutate with simple dataclasses.

 ### Defining a Dataclass

 You can define your dataclasses using the `BaseModel` from Transmutate, which provides built-in serialization and validation capabilities.

 ```python
 from dataclasses import dataclass, field
 from typing import List, Optional
 from transmutate.base_model import BaseModel

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
 ```

 ### JSON Serialization

 Convert a dataclass instance to JSON:

 ```python
 person = Person(name="John Doe", age=30, email="john.doe@example.com")
 json_data = person.to_json()
 print(json_data)
 ```

 Output:

 ```json
 {
     "name": "John Doe",
     "age": 30,
     "email": "john.doe@example.com",
     "phone_numbers": []
 }
 ```

 Parse a JSON string back to a dataclass instance:

 ```python
 person_from_json = Person.from_json(json_data)
 print(person_from_json)
 ```

 ### JSONB Serialization

 Convert a dataclass instance to JSONB:

 ```python
 jsonb_data = person.to_jsonb()
 print(jsonb_data)
 ```

 Output:

 ```json
 {"name":"John Doe","age":30,"email":"john.doe@example.com","phone_numbers":[]}
 ```

 Parse a JSONB string back to a dataclass instance:

 ```python
 person_from_jsonb = Person.from_jsonb(jsonb_data)
 print(person_from_jsonb)
 ```

 ### Proto Serialization

 Generate a Proto definition from a dataclass:

 ```python
 proto_definition = person.to_proto()
 print(proto_definition)
 ```

 Output:

 ```protobuf
 syntax = "proto3";

 message Person {
   string name = 1;
   int32 age = 2;
   string email = 3;
   repeated string phone_numbers = 4;
 }
 ```

 ### Custom Validation

 You can define custom validation logic for fields in your dataclasses using `validation_<field>` methods. These methods will automatically be called during initialization.

 ```python
 @dataclass
 class Address(BaseModel):
     street: str
     city: str
     zip_code: str

     def validation_zip_code(self):
         if not self.zip_code.isdigit() or len(self.zip_code) != 5:
             raise ValueError("Zip code must be a 5-digit number.")
 ```

 ### Defining a gRPC Service

 The `Service` class allows you to define gRPC services with various RPC types.

 ```python
 from transmutate.service import Service, RpcType
 from typing import List

 class TestMessage(BaseModel):
     name: str
     age: int
     email: str
     phone_numbers: List[str]

 class AnotherMessage(BaseModel):
     status: str
     message: str

 service = Service(
     name="TestService",
     types=[RpcType.UNARY, RpcType.SERVER_STREAMING],
     method_names=["GetInfo", "StreamInfo"],
     request_dataclass=TestMessage,
     response_dataclass=AnotherMessage
 )
 ```

 ### Proto File Generation

 Use `ProtoGenerator` to automatically generate Proto files for services and messages.

 ```python
 from transmutate.proto_generator import ProtoGenerator

 services = [
     Service(
         name="TestService",
         types=[RpcType.UNARY, RpcType.SERVER_STREAMING],
         method_names=["GetInfo", "StreamInfo"],
         request_dataclass=TestMessage,
         response_dataclass=AnotherMessage
     )
 ]

 proto_generator = ProtoGenerator(service_name="TestService", services=services)
 proto_generator.generate_proto()
 ```

 Output Proto file will be saved in the specified directory:

 ```
 syntax = "proto3";

 package testservice;

 service TestService {
   rpc GetInfo (TestMessage) returns (AnotherMessage);
   rpc StreamInfo (TestMessage) returns (stream AnotherMessage);
 }

 message TestMessage {
   string name = 1;
   int32 age = 2;
   string email = 3;
   repeated string phone_numbers = 4;
 }

 message AnotherMessage {
   string status = 1;
   string message = 2;
 }
 ```

 ### Testing

 Transmutate includes a suite of unit tests to ensure functionality. You can run the tests using `unittest` or `pytest`.

 ```bash
 # Using unittest
 poetry run python -m unittest discover tests

 # Using pytest
 poetry run pytest tests
 ```

 ## Contributing

 Contributions to Transmutate are welcome! Please feel free to open issues or submit pull requests on the GitHub repository.

 ## License

 Transmutate is open-source software licensed under the MIT License.
