from dataclasses import fields


class ValidationMixin:
    def __init__(self, model):
        self.model = model

    def run_validations(self):
        """
        Runs all dynamic validations on the instance's fields.
        """
        for field_info in fields(self.model):
            validation_method_name = f"validation_{field_info.name}"
            validation_method = getattr(self.model, validation_method_name, None)
            if callable(validation_method):
                validation_method(getattr(self.model, field_info.name))
