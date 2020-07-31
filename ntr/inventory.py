import uuid
from typing import Iterable


class Item:
    id = None
    title = None

    def __init__(self, title: str):
        # Random, globally unique ID for each item instance
        self.id = str(uuid.uuid1())
        self.title = title


class Inventory:
    items = None

    def __init__(self, items: Iterable[Item] = None):
        self.items = {}

        if items:
            for i in items:
                self.items[i.id] = i

    def add_item(self, item: Item):
        self.items[item.id] = item

    def remove_item(self, id_):
        if id_ in self.items:
            del self.items[id_]
        else:
            return False

    def find_item(self, predicate):
        """Return the first item that matches some condition based on the
        predicate passed as argument.

        Example:
            # Return first item that has string "wilson" in its title.
            self.find_item(lambda item: "wilson" in item.title)
        """
        for v in self.items.values():
            if predicate(v):
                return v

    def get_items(self):
        return self.items

    def delete_all_items(self):
        self.items = {}
