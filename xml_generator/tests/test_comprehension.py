import unittest

from xml_generator import XmlNode


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

    def test_query_creation(self):
        node = XmlNode.from_query('node@attr1="value1"@attr2="value2"')
        self.assertEqual(node.name, "node")
        self.assertEqual(node.attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertIsNone(node.body)
        self.assertIsNone(node.children)

    def test_queries_creation(self):
        nodes = XmlNode.from_queries(
            {
                "node@attr1='value1'@attr2='value2'": {
                    "child1@attr1='value1'": None,
                    "child2@attr2='value2'": None,
                }
            }
        )

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].name, "node")
        self.assertEqual(nodes[0].attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertEqual(len(nodes[0].children), 2)
        self.assertEqual(nodes[0].children[0].name, "child1")
        self.assertEqual(nodes[0].children[1].name, "child2")
        self.assertEqual(nodes[0].children[0].attributes, {"attr1": "value1"})
        self.assertEqual(nodes[0].children[1].attributes, {"attr2": "value2"})
