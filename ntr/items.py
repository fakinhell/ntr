import uuid
from typing import Iterable, Union


class Item:
    id = None
    title = None

    def __init__(self, title: str):
        # Random, globally unique ID for each item instance
        self.id = str(uuid.uuid1())
        self.title = title


class ItemStorage:
    max_capacity = None
    items = None

    def __init__(self, items: Iterable[Item] = None, max_capacity: int = None):
        self.items = {}
        self.max_capacity = max_capacity

        if items:
            for i in items[:self.max_capacity] if self.max_capacity else items:
                self.items[i.id] = i

    def add_item(self, item: Item):
        if self.max_capacity and len(self.items) > self.max_capacity:
            return False

        self.items[item.id] = item

    def remove_item(self, id_):
        if id_ in self.items:
            del self.items[id_]
        else:
            return False

    def find_item(self, predicate) -> Union[Item, None]:
        """Return the first item that matches some condition based on the
        predicate passed as argument.

        Example:
            # Return first item that has string "wilson" in its title.
            self.find_item(lambda item: "wilson" in item.title)
        """
        for v in self.items.values():
            if predicate(v):
                return v

    def find_items(self, predicate) -> set:
        """Return set of all items that match some condition based on the
        predicate passed as argument.

        Example:
            # Return all items that have string "wilson" in its title.
            self.find_items(lambda item: "wilsson" in item.title)
        """
        result = set()
        for v in self.items.values():
            if predicate(v):
                result.add(v)

        return result

    def get_items(self) -> dict:
        return self.items.values()

    def delete_all_items(self) -> None:
        self.items = {}
