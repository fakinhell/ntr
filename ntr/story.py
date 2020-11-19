from ntr.items import ItemStorage, Item


class World:
    _map = None

    def __init__(self, map_) -> None:
        self._map = map_


class Story(object):
    """Class representing a story."""
    _description_text = ""
    _start = None
    _map = {}

    def __init__(self, description_text, start, game_map):
        self._description_text = description_text
        self._start = start
        self._map = game_map


class PlaceNode:
    node_id = ''
    text = ''
    item_storage: ItemStorage = None
    options = None

    def __init__(self, node_id: str, text: str, options: list,
                 item_storage: ItemStorage = None) -> None:
        self.node_id = node_id
        self.text = text
        self.options = options
        self.item_storage = item_storage or ItemStorage([Item('hovno')])

    @property
    def actions(self) -> list:
        actions = []

        for item in self.item_storage.get_items():
            actions.append(item)


class ItemStorageNode(PlaceNode):

    @property
    def text(self):
        items = list(self.item_storage.values())
        if not items:
            return "No items here."

        text = "You're browsing items. There " \
            "are:" if len(items) > 1 else "is:"
        text += ''.join([f'- {i}\n' for i in items])

        return text
