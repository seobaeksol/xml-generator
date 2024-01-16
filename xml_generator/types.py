from __future__ import annotations
from typing import Any


class XmlNode:
    def __init__(
        self,
        name: str,
        attributes: dict = None,
        body: str | list[XmlNode] = None,
    ) -> None:
        self.name = name
        self.attributes = attributes if attributes else {}
        self.body = body

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, XmlNode):
            return False

        return (
            self.name == __value.name
            and self.attributes == __value.attributes
            and self.body == __value.body
        )

    @property
    def children(self) -> list[XmlNode] | None:
        """Return the children of the XmlNode object."""
        if not isinstance(self.body, list):
            return None

        return self.body

    @classmethod
    def parse(cls, data: Any) -> XmlNode:
        """Parse Comprehensive format into an XmlNode object."""
        if isinstance(data, dict):
            return cls(
                data["name"],
                data["attributes"] if "attributes" in data else None,
                XmlNode.parse(data["body"]) if "body" in data else None,
            )

        if isinstance(data, list):
            return [XmlNode.parse(item) for item in data]

        if isinstance(data, str):
            return data

        raise TypeError(f"Cannot parse {type(data)} into XmlNode")

    def find_descendant(self, name: str) -> XmlNode | None:
        """Return the first descendant XmlNode with the given name."""
        if self.children is None:
            return None

        for child in self.children:
            if child.name == name:
                return child

            descendant = child.find_descendant(name)
            if descendant is not None:
                return descendant

        return None

    def find(self, query: str) -> XmlNode | None:
        """
        Return the first XmlNode with the given query.
        Query can be a name with attributes.
        """
        if XmlNode.check(self, query):
            return self

        if self.children is None:
            return None

        for child in self.children:
            if child.name == query:
                return child

            descendant = child.find(query)
            if descendant is not None:
                return descendant

        return None

    @classmethod
    def check(cls, node: XmlNode, query: str) -> bool:
        """
        Check if the XmlNode has the given query.
        Query can be a name or a path.
        Query consists of a name and a list of attributes.
        Attributes are separated by a at sign.
        Ex) node_name@attr1@attr2
        """
        if "@" in query:
            name, *attributes = query.split("@")
        else:
            name = query
            attributes = []

        if node.name != name:
            return False

        for attribute in attributes:
            if attribute not in node.attributes:
                return False

        return True

    def to_xml(
        self,
        depth: int = 0,
        declaration: bool = False,
        indent_char: str = " ",
        indent_size: int = 4,
        declaration_tag: str = '<?xml version="1.0" encoding="UTF-8"?>\n',
    ) -> str:
        """Return the XmlNode as an XML string."""
        xml = declaration_tag if declaration else ""
        indent = indent_char * indent_size * depth

        if self.body is None:
            xml += f"{indent}<{self.name} {self._attributes_to_xml()}/>\n"
        elif isinstance(self.body, str):
            xml += f"{indent}<{self.name} {self._attributes_to_xml()}>{self.body}</{self.name}>\n"
        elif isinstance(self.body, list):
            xml += f"{indent}<{self.name} {self._attributes_to_xml()}>\n"
            for child in self.body:
                xml += child.to_xml(
                    depth + 1, indent_char=indent_char, indent_size=indent_size
                )
            xml += f"{indent}</{self.name}>\n"

        if depth == 0:
            xml = xml.strip()

        return xml

    def _attributes_to_xml(self) -> str:
        """Return the XmlNode's attributes as an XML string."""
        return " ".join(f'{key}="{value}"' for key, value in self.attributes.items())
