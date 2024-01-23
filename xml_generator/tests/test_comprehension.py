import unittest

import sys

sys.path.append("../../")
sys.path.append("../")
sys.path.append("C:\\Users\\F2023027\\Desktop\\Projects\\xml-generator")
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
        """Test XmlNode.from_query() with a query format."""
        node = XmlNode.from_query('node@attr1="value1"@attr2="value2"')
        self.assertEqual(node.name, "node")
        self.assertEqual(node.attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertIsNone(node.body)
        self.assertIsNone(node.children)

    def test_extend_query_creation(self):
        """Test XmlNode.from_extend_query() with a query format."""
        nodes = XmlNode.from_extend_query(
            [
                "NoValueNode",
                {
                    "SHORT-NAME": "node",
                },
                {
                    "ELEMENTS@type='string'": [
                        "element@hint='id'",
                        "element@unit='m'",
                        {"element@unit='m'@min='0'@max='100'@init='50'": "100"},
                    ],
                },
            ]
        )

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].name, "NoValueNode")
        self.assertIsNone(nodes[0].body)
        self.assertEqual(nodes[1].name, "SHORT-NAME")
        self.assertEqual(nodes[1].body, "node")
        self.assertEqual(len(nodes[2].children), 3)
        self.assertEqual(nodes[2].children[0].name, "element")
        self.assertEqual(nodes[2].children[1].name, "element")
        self.assertEqual(nodes[2].children[0].attributes, {"hint": "id"})
        self.assertEqual(nodes[2].children[1].attributes, {"unit": "m"})
        self.assertEqual(
            nodes[2].children[2].attributes,
            {"unit": "m", "min": "0", "max": "100", "init": "50"},
        )
        self.assertEqual(nodes[2].children[2].body, "100")

    def test_extend_query_appendent(self):
        """Test XmlNode.append_extend_query() with a query format."""
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

        nodes = node.append_extend_query(
            [
                "NoValueNode",
                {
                    "SHORT-NAME": "node",
                },
                {
                    "ELEMENTS@type='string'": [
                        "element@hint='id'",
                        "element@unit='m'",
                        {"element@unit='m'@min='0'@max='100'@init='50'": "100"},
                    ],
                },
            ]
        )

        self.assertEqual(len(node.children), 5)
        self.assertEqual(nodes, node.children[2:])
