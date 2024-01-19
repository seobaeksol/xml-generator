from __future__ import annotations
from typing import Any, override
from xml.etree.ElementTree import TreeBuilder


Query = str
QueryDict = dict[Query, dict | str | None]


class XmlNode:
    def __init__(
        self,
        name: str,
        attributes: dict = None,
        body: str | list[XmlNode] = None,
        parent: XmlNode = None,
    ) -> None:
        self.name = name
        self.attributes = attributes if attributes else {}
        self.body = body
        self.parent = parent

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
        """Parse Comprehensive format into an XmlNode object.
        Ex)
        XmlNode.parse(
        {
            "name": "node",
            "attributes": {"attr1": "value1", "attr2": "value2"},
            "body": [
                {"name": "child1", "attributes": {"attr1": "value1"}},
                {"name": "child2", "attributes": {"attr2": "value2"}},
            ],
        }
        """
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
        Ex) node_name@attr1=value1@attr2
        : find a node with the name node_name that has the attributes attr1 and attr2
          and attr1 has the value value1. (attr2 just needs to exist)
        """
        if "@" in query:
            name, *attributes = query.split("@")
        else:
            name = query
            attributes = []

        if node.name != name:
            return False

        for attribute in attributes:
            if "=" in attribute:
                attr_key, attr_value = attribute.split("=")
            else:
                attr_key = attribute
                attr_value = None

            if attr_key not in node.attributes:
                return False

            # No attribute value means that the attribute just needs to exist
            if attr_value is not None and node.attributes[attr_key] != attr_value:
                return False

        return True

    @classmethod
    def from_query(cls, query: str) -> XmlNode:
        """
        Return the XmlNode with the given query.
        Query can be a name with attributes.
        Ex) node_name@attr1=value1@attr2
        : find a node with the name node_name that has the attributes attr1 and attr2
          and attr1 has the value value1. (attr2 just needs to exist)
        """
        if "@" in query:
            name, *raw_attributes = query.split("@")
        else:
            name = query
            raw_attributes = []

        attributes = {}
        for attribute in raw_attributes:
            if "=" in attribute:
                attr_key, attr_value = attribute.split("=")
            else:
                attr_key = attribute
                attr_value = None

            attributes[attr_key] = (
                attr_value.removeprefix('"')
                .removesuffix('"')
                .removeprefix("'")
                .removesuffix("'")
                if attr_value is not None
                else None
            )

        return XmlNode(name, attributes)

    def to_xml(
        self,
        depth: int = 0,
        declaration: bool = False,
        indent_char: str = " ",
        indent_size: int = 4,
        declaration_tag: str = '<?xml version="1.0" encoding="utf-8"?>\n',
    ) -> str:
        """
        Return the XmlNode as an XML string.
        TODO: remove tag end spaces
        """
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

    def get_or_create_with_queries(self, queries: list[str]) -> XmlNode:
        """Return the XmlNode with the given names."""
        node = self
        for query in queries:
            if node.children is None:
                node.body = []
            found_child = next(
                (child for child in node.children if XmlNode.check(child, query)), None
            )
            if found_child is None:
                found_child = XmlNode.from_query(query)
                node.body.append(found_child)
            node = found_child
        return node

    @classmethod
    def from_queries(cls, queries: list[str | dict]) -> list[XmlNode]:
        """
        Return the XmlNode with the given queries.
        ex) queries = [
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
        ]
        """
        nodes = []
        if not isinstance(queries, list):
            raise TypeError(
                f"Cannot parse {type(queries)} into XmlNode, it must be a list"
            )

        for query in queries:
            if isinstance(query, str):
                nodes.append(XmlNode.from_query(query))
            elif isinstance(query, dict):
                for key, value in query.items():
                    node = XmlNode.from_query(key)
                    if value is None:
                        nodes.append(node)
                    elif isinstance(value, str):
                        node.body = value
                        nodes.append(node)
                    elif isinstance(value, list):
                        node.body = XmlNode.from_queries(value)
                        nodes.append(node)

        return nodes

    def append_queries(self, queries: list[str | dict]) -> list[XmlNode]:
        """
        With the given queries, append the XmlNode objects into children and return it.
        ex) queries = [
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
        ]
        """
        if self.children is None:
            self.body = []

        if isinstance(self.body, str):
            raise ValueError("Cannot append queries to a XmlNode with a body string")

        nodes = XmlNode.from_queries(queries)

        self.body.extend(nodes)

        return nodes

    def __str__(self) -> str:
        body_info = (
            self.body if isinstance(self.body, str) else f"children={len(self.body)}"
        )

        return (
            f"XmlNode(name={self.name}, attributes={self.attributes}, body={body_info})"
        )


class XmlParser(TreeBuilder):
    default_ns = ""
    ns_stack = []
    ns_dict = {}
    current = None

    @override
    def start(self, tag, attrs):
        name = tag.replace(f"{{{self.default_ns}}}", "")
        # Handle root's namespace
        if self.current is None:
            new_attrs = {}
            if self.default_ns:
                new_attrs["xmlns"] = self.default_ns

            for prefix, uri in self.ns_dict.items():
                new_attrs[f"xmlns:{prefix}"] = uri

            for prefix, uri in self.ns_dict.items():
                for key, value in attrs.items():
                    if key.startswith(f"{{{uri}}}"):
                        new_attrs[key.replace(f"{{{uri}}}", f"{prefix}:")] = value

            self.current = XmlNode(name, new_attrs)
            return

        self.current = XmlNode(name, attrs, parent=self.current)
        if self.current.parent is None:
            return

        if not isinstance(self.current.parent.body, list):
            self.current.parent.body = []
        self.current.parent.body.append(self.current)

    @override
    def start_ns(self, prefix, uri):
        if prefix == "":
            self.default_ns = uri
        else:
            self.ns_stack.append((prefix, uri))
            self.ns_dict[prefix] = uri

    @override
    def end_ns(self, prefix):
        if prefix != "":
            self.ns_stack.pop()

    @override
    def end(self, tag):
        if self.current.parent is not None:
            self.current = self.current.parent

    @override
    def data(self, data):
        if not data.isspace():
            self.current.body = data

    @override
    def close(self):
        return self.current
