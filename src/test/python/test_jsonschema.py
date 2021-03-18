from unittest import TestCase
from jsonschema import validate, ValidationError


class JsonSchemaExampleTest(TestCase):
    schema = {
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"},
        },
    }

    def test_validate_should_be_ok(self):
        validate(instance={"name": "Eggs", "price": 34.99}, schema=self.schema)

    def test_validate_should_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            validate(instance={"name": "Eggs", "price": "Invalid"}, schema=self.schema)
