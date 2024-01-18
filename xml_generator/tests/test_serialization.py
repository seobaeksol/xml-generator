import unittest

from xml_generator.tests.utils import create_sample_node


class SerializationTestCase(unittest.TestCase):
    def test_simple_generation(self):
        """Test XmlNode.to_xml() with a simple format."""
        root = create_sample_node()

        with open("xml_generator/tests/samples/simple.xml", "r", encoding="utf-8") as f:
            expected = f.read()

        self.assertEqual(root.to_xml(), expected)

    def test_simple_generation_with_declaration(self):
        """Test XmlNode.to_xml() with a simple format and declaration."""
        root = create_sample_node()

        with open(
            "xml_generator/tests/samples/simple_with_declaration.xml",
            "r",
            encoding="utf-8",
        ) as f:
            expected = f.read()

        self.assertEqual(root.to_xml(declaration=True), expected)
