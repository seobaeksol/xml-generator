from xml_generator.types import XmlNode


def create_sample_node():
    return XmlNode.parse(
        {
            "name": "node",
            "attributes": {"attr1": "value1", "attr2": "value2"},
            "body": [
                {"name": "child1", "attributes": {"attr1": "value1"}},
                {"name": "child2", "attributes": {"attr2": "value2"}},
            ],
        }
    )
