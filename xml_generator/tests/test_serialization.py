import unittest

from xml_generator.tests.utils import create_sample_node
from xml_generator.types import XmlNode


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

    def test_dict_type_convertion(self):
        """Test XmlNode.parse() with a dictionary value."""
        node = XmlNode.from_extended_query(
            [
                {
                    "TRANSMISSION-MODE-FALSE-TIMING": {
                        "EVENT-CONTROLLED-TIMING": {"NUMBER-OF-REPETITIONS": "0"}
                    }
                },
                {
                    "TRANSMISSION-MODE-TRUE-TIMING": {
                        "EVENT-CONTROLLED-TIMING": {"NUMBER-OF-REPETITIONS": "0"}
                    }
                },
            ]
        )

        self.assertEqual(
            node[0].to_xml(),
            "<TRANSMISSION-MODE-FALSE-TIMING>\n    <EVENT-CONTROLLED-TIMING>\n        <NUMBER-OF-REPETITIONS>0</NUMBER-OF-REPETITIONS>\n    </EVENT-CONTROLLED-TIMING>\n</TRANSMISSION-MODE-FALSE-TIMING>",
        )
        self.assertEqual(
            node[1].to_xml(),
            "<TRANSMISSION-MODE-TRUE-TIMING>\n    <EVENT-CONTROLLED-TIMING>\n        <NUMBER-OF-REPETITIONS>0</NUMBER-OF-REPETITIONS>\n    </EVENT-CONTROLLED-TIMING>\n</TRANSMISSION-MODE-TRUE-TIMING>",
        )
