import unittest

from xml_generator.types import XmlNode


class ComprehensionTestCase(unittest.TestCase):
    def test_comprehensive_creation(self):
        """Test XmlNode.parse() with a comprehensive format."""
        node = XmlNode.parse(
            {
                "name": "node",
                "attributes": {"attr1": "value1", "attr2": "value2"},
                "body": [
                    {"name": "child1", "attributes": {"attr1": "value1"}},
                    {"name": "child2", "attributes": {"attr2": "value2"}},
                ],
            }
        )

        self.assertEqual(node.name, "node")
        self.assertEqual(node.attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].name, "child1")
        self.assertEqual(node.children[1].name, "child2")
        self.assertEqual(node.children[0].attributes, {"attr1": "value1"})
        self.assertEqual(node.children[1].attributes, {"attr2": "value2"})
