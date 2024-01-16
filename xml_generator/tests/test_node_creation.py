import unittest

from xml_generator import XmlNode
from xml_generator.tests.utils import create_sample_node


class NodeCreationTestCase(unittest.TestCase):
    """Test case for the creation of XmlNode objects."""

    def test_simple_creation(self):
        """Test XmlNode creation without attributes, body, or children."""
        node = XmlNode("node")
        self.assertEqual(node.name, "node")

    def test_creation_with_attributes(self):
        """Test XmlNode creation with attributes."""
        node = XmlNode("node", {"attr1": "value1", "attr2": "value2"})
        self.assertEqual(node.name, "node")
        self.assertEqual(node.attributes, {"attr1": "value1", "attr2": "value2"})

    def test_creation_with_body(self):
        """Test XmlNode creation with body."""
        node = XmlNode("node", body="body")
        self.assertEqual(node.name, "node")
        self.assertEqual(node.body, "body")

    def test_creation_with_attributes_and_body(self):
        """Test XmlNode creation with attributes and body."""
        node = XmlNode("node", {"attr1": "value1", "attr2": "value2"}, "body")
        self.assertEqual(node.name, "node")
        self.assertDictEqual(node.attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertEqual(node.body, "body")

    def test_creation_with_children(self):
        """Test XmlNode creation with children."""
        node = XmlNode("node", body=[XmlNode("child")])
        self.assertEqual(node.name, "node")
        self.assertListEqual(node.children, [XmlNode("child")])

    def test_creation_with_attributes_and_children(self):
        """Test XmlNode creation with attributes and children."""
        node = XmlNode(
            "node", {"attr1": "value1", "attr2": "value2"}, [XmlNode("child")]
        )
        self.assertEqual(node.name, "node")
        self.assertDictEqual(node.attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertListEqual(node.children, [XmlNode("child")])


class SubTagCreationTestCase(unittest.TestCase):
    def test_creation_sub_tags_with_names(self):
        """Test XmlNode creation with sub tags."""
        root = create_sample_node()

        root.get_or_create_with_queries(["child1", "child3", "child4"])
        self.assertEqual(len(root.children), 2)
        self.assertEqual(len(root.children[0].children), 1)
        self.assertEqual(len(root.children[0].children[0].children), 1)
        self.assertEqual(root.children[0].children[0].name, "child3")
        self.assertEqual(root.children[0].children[0].children[0].name, "child4")

    def test_creation_sub_tags_with_queries(self):
        """Test XmlNode creation with sub tags using query syntax."""
        root = create_sample_node()

        root.get_or_create_with_queries(["child1@attr1", "child3@attr3", "child4"])
        self.assertEqual(len(root.children), 2)
        self.assertEqual(len(root.children[0].children), 1)
        self.assertEqual(len(root.children[0].children[0].children), 1)
        self.assertTrue(XmlNode.check(root.children[0].children[0], "child3@attr3"))
        self.assertTrue(
            XmlNode.check(root.children[0].children[0].children[0], "child4")
        )
