from unittest import TestCase
import yaml


class PyYamlExampleTest(TestCase):
    raw_data = """
    type: object
    properties:
        price:
            type: number
        name:
            type: string
    """

    data = {
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"},
        },
    }

    def test_read(self):
        data = yaml.load(self.raw_data, Loader=yaml.FullLoader)
        self.assertDictEqual(data, self.data)
