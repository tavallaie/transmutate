import os
from typing import List
from transmutate import Service


class ProtoGenerator:
    def __init__(self, service_name: str, services: List[Service], output_dir="protos"):
        """
        Initializes the ProtoGenerator with service name, methods, and output directory.

        :param service_name: Name of the gRPC service.
        :param services: List of Service dataclass instances.
        :param output_dir: Directory to save the generated proto file.
        """
        self.service_name = service_name
        self.services = services
        self.output_dir = output_dir
        self.proto_file_path = os.path.join(output_dir, f"{service_name.lower()}.proto")

    def generate_proto(self):
        """
        Generates the proto file content and writes it to the specified output directory.
        """
        proto_content = (
            self._generate_header()
            + self._generate_service()
            + self._generate_messages()
        )
        self._write_proto_file(proto_content)
        print(f"Proto file generated: {self.proto_file_path}")

    def _generate_header(self) -> str:
        """
        Generates the header for the proto file.

        :return: Header content as a string.
        """
        return f"""
syntax = "proto3";

package {self.service_name.lower()};

// {self.service_name} service definition
"""

    def _generate_service(self) -> str:
        """
        Generates the service definition with RPC methods.

        :return: Service definition content as a string.
        """
        service_content = f"service {self.service_name} {{\n"

        for service in self.services:
            request_message_name = (
                service.request_dataclass.__name__
                if service.request_dataclass
                else "Empty"
            )
            response_message_name = (
                service.response_dataclass.__name__
                if service.response_dataclass
                else "Empty"
            )

            for rpc_type, method_name in zip(
                service.types, service.method_names
            ):  # Iterate over types and names
                rpc_definition = (
                    rpc_type.value
                )  # Get the template directly from the enum

                if rpc_definition:
                    service_content += rpc_definition.format(
                        method_name=method_name,
                        request_message=request_message_name,
                        response_message=response_message_name,
                    )

        service_content += "}\n\n"
        return service_content

    def _generate_messages(self) -> str:
        """
        Generates message definitions for requests and responses using the to_proto function.

        :return: Message definitions as a string.
        """
        messages_content = "// Request and response messages\n"

        unique_messages = set()

        for service in self.services:
            if (
                service.request_dataclass
                and service.request_dataclass.__name__ not in unique_messages
            ):
                unique_messages.add(service.request_dataclass.__name__)
                request_instance = service.request_dataclass()
                messages_content += request_instance.to_proto()

            if (
                service.response_dataclass
                and service.response_dataclass.__name__ not in unique_messages
            ):
                unique_messages.add(service.response_dataclass.__name__)
                response_instance = service.response_dataclass()
                messages_content += response_instance.to_proto()

        return messages_content

    def _write_proto_file(self, content: str):
        """
        Writes the proto content to a file.

        :param content: The complete proto content as a string.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        with open(self.proto_file_path, "w") as proto_file:
            proto_file.write(content)
