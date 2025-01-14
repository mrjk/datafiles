"""Tests that represent usage as an ORM."""

from dataclasses import dataclass

from datafiles import datafile
from datafiles.utils import logbreak


# This model is based on the example dataclass from:
# https://docs.python.org/3/library/dataclasses.html
@datafile('../tmp/inventory/{self.pk}.yml')
class InventoryItem:
    pk: int
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


def test_multiple_instances_are_distinct(expect):
    item_1 = InventoryItem.objects.get_or_create(1, "Nuts", 0.23)
    item_2 = InventoryItem.objects.get_or_create(2, "Bolts", 0.45, quantity_on_hand=100)

    expect(item_1.datafile.data) == {'name': 'Nuts', 'unit_price': 0.23}
    expect(item_2.datafile.data) == {
        'name': 'Bolts',
        'unit_price': 0.45,
        'quantity_on_hand': 100,
    }

    item_1.quantity_on_hand = 200
    item_2.unit_price = 0.34

    expect(item_1.datafile.data) == {
        'name': 'Nuts',
        'unit_price': 0.23,
        'quantity_on_hand': 200,
    }
    expect(item_2.datafile.data) == {
        'name': 'Bolts',
        'unit_price': 0.34,
        'quantity_on_hand': 100,
    }


def test_classes_can_share_a_nested_dataclass(expect):
    @dataclass
    class Nested:
        value: int

    @datafile('../tmp/sample.json')
    class Foo:
        nested: Nested

    logbreak("Initialize Foo")
    foo = Foo(Nested(1))

    expect(foo.nested.value) == 1

    @datafile('../tmp/sample.toml')
    class Bar:
        nested: Nested

    logbreak("Initialize Bar")
    bar = Bar(Nested(2))

    expect(bar.nested.value) == 2
