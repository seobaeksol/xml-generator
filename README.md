# XML Generator

Comprehensive XML generator for Python

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install xml-generator
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

Parse Comprehensive format with quries

```python
node = XmlNode.from_query('node@attr1="value1"@attr2="value2"')
```

```python
nodes = XmlNode.from_queries(
    [
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
)
```

### Searching a specific node

Return the first XmlNode with the given query. Query can be a name with attributes.

```python
parent = node.find("node")
child1 = node.find("child1@attr1")
child2 = node.find("child2")
```

### Generate a xml file

Using the `to_xml()` function that return the XmlNode as an XML string.

```python
with open('sample.xml', 'w', encoding='utf-8') as f:
    f.write(node.to_xml())
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
