import unittest
from xml.etree.ElementTree import XMLParser

from xml_generator.types import XmlParser


class DeserializationTestCase(unittest.TestCase):
    def test_simple_generation(self):
        my_parser = XmlParser()
        parser = XMLParser(target=my_parser)

        with open(
            file="xml_generator/tests/samples/complex.xml", mode="r", encoding="utf-8"
        ) as f:
            original_xml = f.read()
            parser.feed(original_xml)
        root = parser.close()

        xml_string = root.to_xml(
            declaration=True,
        )

        self.assertEqual(xml_string, original_xml)
