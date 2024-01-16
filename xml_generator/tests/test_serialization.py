import unittest

from xml_generator.tests.utils import create_sample_node

EXPECTED_SIMPLE_XML = """
<node attr1="value1" attr2="value2">
    <child1 attr1="value1"/>
    <child2 attr2="value2"/>
</node>
""".strip()


EXPECTED_SIMPLE_XML_WITH_DECLARATION = """
<?xml version="1.0" encoding="UTF-8"?>
<node attr1="value1" attr2="value2">
    <child1 attr1="value1"/>
    <child2 attr2="value2"/>
</node>
""".strip()


class SerializationTestCase(unittest.TestCase):
    def test_simple_generation(self):
        """Test XmlNode.to_xml() with a simple format."""
        root = create_sample_node()
        self.assertEqual(
            root.to_xml(), EXPECTED_SIMPLE_XML, "Generated XML does not match expected"
        )

    def test_simple_generation_with_declaration(self):
        """Test XmlNode.to_xml() with a simple format and declaration."""
        root = create_sample_node()
        self.assertEqual(
            root.to_xml(declaration=True),
            EXPECTED_SIMPLE_XML_WITH_DECLARATION,
            "Generated XML does not match expected",
        )
