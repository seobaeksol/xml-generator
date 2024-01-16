import unittest

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


class SearchTestCase(unittest.TestCase):
    def test_find_decendant(self):
        """Test XmlNode.find_decendant()"""
        root = create_sample_node()

        child1 = root.find_descendant("child1")
        child2 = root.find_descendant("child2")

        # Test that the children were found
        self.assertIsNotNone(child1)
        self.assertIsNotNone(child2)

        # Test that the children are correct
        self.assertEqual(child1.name, "child1")
        self.assertEqual(child2.name, "child2")
        self.assertEqual(child1.attributes, {"attr1": "value1"})
        self.assertEqual(child2.attributes, {"attr2": "value2"})

    def test_find(self):
        """Test XmlNode.find()"""
        root = create_sample_node()

        parent = root.find("node")
        child1 = root.find("child1@attr1")
        child2 = root.find("child2")

        # Test that the children were found
        self.assertIsNotNone(parent)
        self.assertIsNotNone(child1)
        self.assertIsNotNone(child2)

        # Test that the results are correct
        self.assertEqual(parent.name, "node")
        self.assertEqual(child1.name, "child1")
        self.assertEqual(child2.name, "child2")
        self.assertEqual(parent.attributes, {"attr1": "value1", "attr2": "value2"})
        self.assertEqual(child1.attributes, {"attr1": "value1"})
        self.assertEqual(child2.attributes, {"attr2": "value2"})


class FailureSearchTestCase(unittest.TestCase):
    def test_find_decendant(self):
        """Test XmlNode.find_decendant() with a bad query"""
        root = create_sample_node()

        self.assertIsNone(root.find_descendant("child3"))

    def test_find(self):
        """Test XmlNode.find() with a bad query"""
        root = create_sample_node()

        self.assertIsNone(root.find("child1@attr2"))
