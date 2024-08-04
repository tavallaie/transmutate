from dataclasses import fields


class ValidationMixin:
    def run_validations(self):
        """
        Runs all dynamic validations on the instance's fields.
        """
        for field_info in fields(self):
            validation_method_name = f"validation_{field_info.name}"
            validation_method = getattr(self, validation_method_name, None)
            if callable(validation_method):
                validation_method(getattr(self, field_info.name))
