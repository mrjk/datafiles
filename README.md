# Datafiles: A file-based ORM for dataclasses

Datafiles is a bidirectional serialization library for Python [dataclasses](https://docs.python.org/3/library/dataclasses.html) to synchronizes objects to the filesystem using type annotations. It supports a variety of file formats with round-trip preservation of formatting and comments, where possible. Object changes are automatically saved to disk and only include the minimum data needed to restore each object.

[![PyPI Version](https://img.shields.io/pypi/v/datafiles.svg)](https://pypi.org/project/datafiles)
[![PyPI License](https://img.shields.io/pypi/l/datafiles.svg)](https://pypi.org/project/datafiles)
[![Travis CI](https://img.shields.io/travis/jacebrowning/datafiles/develop.svg?label=unix)](https://travis-ci.org/jacebrowning/datafiles)
[![AppVeyor](https://img.shields.io/appveyor/ci/jacebrowning/datafiles/develop.svg?label=windows)](https://ci.appveyor.com/project/jacebrowning/datafiles)
[![Coveralls](https://img.shields.io/coveralls/jacebrowning/datafiles.svg)](https://coveralls.io/r/jacebrowning/datafiles)

Popular use cases include:

- Coercing user-editable files into the proper Python types
- Storing program configuration and data in version control
- Loading data fixtures for demonstration or testing purposes
- Prototyping data models agnostic of persistance backends

## Overview

Take an existing dataclass such as [this example](https://docs.python.org/3/library/dataclasses.html#module-dataclasses) from the documentation:

```python
from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""

    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

and decorate it with directory pattern to synchronize instances:

```python
from datafiles import datafile

@datafile("inventory/items/{self.name}.yml")
@dataclass
class InventoryItem:
    ...
```

Then, work with instances of the class as normal:

```python
>>> item = InventoryItem("widget", 3)
```

```yaml
# inventory/items/widget.yml

unit_price: 3.0
```

Changes to the object are automatically saved to the filesystem:

```python
>>> item.quantity_on_hand += 100
```

```yaml
# inventory/items/widget.yml

unit_price: 3.0
quantity_on_hand: 100
```

Changes to the filesystem are automatically reflected in the object:

```yaml
# inventory/items/widget.yml

unit_price: 2.5  # <= manually changed from "3.0"
quantity_on_hand: 100
```

```python
>>> item.unit_price
2.5
```

Objects can also be restored from the filesystem:

```python
>>> from datafiles import Missing
>>> item = InventoryItem("widget", Missing)
>>> item.unit_price
2.5
>>> item.quantity_on_hand
100
```

Demo: [Jupyter Notebook](https://github.com/jacebrowning/datafiles/blob/develop/notebooks/readme.ipynb)

## Installation

Because datafiles relies on dataclasses and type annotations, Python 3.7+ is required. Install this library directly into an activated virtual environment:

```
$ pip install datafiles
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```
$ poetry add datafiles
```

## Documentation

To see additional syncrhonization and formatting options, please consult the [full documentation](https://datafiles.readthedocs.io).
