# XML Generator

Comprehensive XML generator for Python

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install xml-generator-seobaeksol
```

## Usage

### Import

```python
from xml_generator.types import XmlNode
```

### Comprehensive parsing

Parse Comprehensive format into an XmlNode object.

```python
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
```

Create a XmlNode with a query

```python
node = XmlNode.from_query('node@attr1="value1"@attr2="value2"')
```

Create a XmlNode with a extended query

```python
extend_query = {
            "root": [
                "NoValueNode",
                {
                    "SHORT-NAME": "node",
                },
                {
                    "ELEMENTS@type=string": [
                        "element@hint=id",
                        "element@unit=m",
                        {"element@unit=m@min=0@max=100@init=50": "100"},
                    ],
                },
            ]
        }
```

### Searching a specific node

Return the first XmlNode with the given query. Query can be a name with attributes.

```python
parent = node.find("node")
child1 = node.find("child1@attr1")
child2 = node.find("child2")
```

### Serialization

Using the `to_xml()` function that return the XmlNode as an XML string.

```python
with open('sample.xml', 'w', encoding='utf-8') as f:
    f.write(node.to_xml())
```

Using the `to_extend_query()` function that return the extended query object as an XML string.

```python
extended_query_obj = root.to_extended_query()
```

### Deserialization

Use `XmlParser` class for reading a xml file that return `XmlNode` by `close()` method.
It is sub-class of `xml.etree.ElementTree.XMLParser` built-in python class.

```python
from xml_generator.types import XmlParser

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
```

## Contributing

Coming soon.

### Testing

```bash
python -m unittest discover -s xml_generator/tests -p "test*.py"
```

### Building

```bash
python .\setup.py sdist bdist_wheel
```

### Deployment

```bash
twine upload dist/*
```

## License

License :: OSI Approved :: MIT License
