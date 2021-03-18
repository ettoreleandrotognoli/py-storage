from unittest import TestCase
import toml


class TomlExampleTest(TestCase):
    raw_data = """
    type = "object"

    [properties.price]
    type = "number"

    [properties.name]
    type = "string"
    """

    data = {
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"},
        },
    }

    def test_read(self):
        data = toml.loads(self.raw_data)
        self.assertDictEqual(data, self.data)
