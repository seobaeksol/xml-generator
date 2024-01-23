import unittest
from xml_generator.types import XmlParser


class DeserializationTestCase(unittest.TestCase):
    def test_xml_parsing_and_dump(self):
        """Test XmlParser and XmlNode.to_xml() with a complex format."""
        parser = XmlParser()

        with open(
            file="xml_generator/tests/samples/complex.xml", mode="r", encoding="utf-8"
        ) as f:
            original_xml = f.read()
            parser.feed(original_xml)
        root = parser.close()

        xml_string = root.to_xml(
            declaration=True, declaration_tag='<?xml version="1.0" encoding="UTF-8"?>\n'
        )

        parser = XmlParser()
        parser.feed(xml_string)
        root2 = parser.close()

        self.assertEqual(root, root2)
