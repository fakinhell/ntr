import string
from typing import Iterable, Optional, Dict

from ntr.items import Item, ItemStorage
from ntr.characters import Character, Player


class World:
    nodes = None

    def __init__(self, nodes) -> None:
        self.nodes = nodes


class Story(object):
    """Class representing a story."""
    description: str = ''
    start: str = None
    nodes: dict = {}

    def __init__(self, description, start, game_nodes):
        self.description = description
        self.start = start
        self.nodes = game_nodes


class GameplayFactory:

    @classmethod
    def build(cls, story: Story) -> 'Gameplay':
        story.nodes = {k: v for k, v in map(cls._build_place_node,
                       story.nodes.items())}
        return Gameplay(story)

    @staticmethod
    def _build_place_node(node_tuple):
        node_id = node_tuple[0]
        node_info = node_tuple[1]

        text = node_info.get('text', '')
        text = '\n'.join(text) if isinstance(text, list) else text

        options = node_info.get('options', [])

        actions = []
        for option in options:
            actions.append(GotoAction(option['label'], option['goto']))

        actions = actions

        return node_id, PlaceNode(text=text, static_actions=actions)


class Gameplay:
    story = None
    world = None
    player = None

    def __init__(self, story: Story):
        self.story = story
        self.nodes = story.nodes
        self.player = Player()

    def run(self):
        node = self.nodes[self.story.start]
        previous_node = None

        while True:
            action = node.run(self.player)

            # If running node returned None, no action was determined and that
            # means "do nothing".
            if action is None:
                continue

            # Result of action being resolved is either an instance of Node
            # or None (do nothing) or False (exit game loop).
            resolved = action.resolve(self.story, self.player)

            # If resolving action returned None (i.e. returned no Node to move
            # to), stay in the current node.
            if resolved is None:
                continue

            if resolved is False:
                break

            if resolved == "@back":
                node = previous_node
                continue

            previous_node = node

            # At this point we're sure the 'resolved' variable contains Node
            # instance. Let's go there.
            node = resolved


class Action:
    """Base class for all actions. Should not be ever instantiated directly.
    """
    #: Human-readable label for this action.
    label: str = None

    def __init__(self, label: str):
        self.label = label

    def resolve(self, story: Story, character: Character):
        raise NotImplementedError


class LambdaAction(Action):
    """Universal action object for custom actions that are resolved by
    executing the lambda function passed as argument.
    """
    fn: callable = None

    def __init__(self, label: str, fn: callable):
        super().__init__(label)
        self.fn = fn

    def resolve(self, story: Story, character: Character):
        return self.fn(story, character)


class GoBackAction(Action):
    def __init__(self, label: str):
        super().__init__(label)

    def resolve(self, story: Story, character: Character):
        return "@back"


class GotoAction(Action):
    goto: str = None

    def __init__(self, label: str, goto: str):
        super().__init__(label)
        self.goto = goto

    def resolve(self, story: Story, character: Character):
        # TODO: Deal with "@back" which doesn't exist as a key in nodes dict,
        # but is a special construct that's handled by the main loop.
        return story.nodes[self.goto]


class BrowseItemsAction(Action):
    item_storage: ItemStorage

    def __init__(self, label: str, item_storage: ItemStorage):
        super().__init__(label)
        self.item_storage = item_storage

    def resolve(self, story: Story, character: Character):
        return ItemStorageNode(self.item_storage)


class Actions:
    """
    Named `Choices` originally (see https://www.youtube.com/watch?v=JenXIQazv2o)
    """
    actions: Dict[str, Action] = None

    def __init__(self, actions: Iterable[Action]):
        self.actions = {string.ascii_letters[i]: a for i, a in
                        enumerate(actions)}

    def __iter__(self):
        """Yield tuples of (<keyboard key>, <action human-readable label>) for
        each action in this actions container.

        To be used for presenting possible actions that can be chosen.
        """
        return ((key, a.label) for key, a in self.actions.items())

    def get(self, key) -> Optional[dict]:
        """Return action object stored under some key, or None, if such key
        doesn't point to any existing action."""
        return self.actions.get(key)


class PlaceNode:
    text = ''
    item_storage: ItemStorage = None
    static_actions = None

    def __init__(self, text: str, static_actions: Actions,
                 item_storage: ItemStorage = None) -> None:
        self.text = text
        self.static_actions = static_actions
        self.item_storage = item_storage or ItemStorage([Item('hovno')])

    def run(self, character):
        all_actions = Actions([*self.static_actions, *self.dynamic_actions])

        character_action = character.turn(self.text, all_actions)

        # Return action object the character has chosen, or None, if the
        # character.turn() did not return anything that points to an available
        # action.
        return all_actions.get(character_action)

    @property
    def dynamic_actions(self):
        result = []
        if self.item_storage.has_items():
            result.append(BrowseItemsAction('Browse items', self.item_storage))

        return result


class ItemStorageNode:
    item_storage: ItemStorage = None
    text = "You're browsing items."

    def __init__(self, item_storage: ItemStorage) -> None:
        self.item_storage = item_storage

    def run(self, character):
        actions = Actions(self.storage_actions)
        player_action = character.turn(self.text, actions)

        # Return action object the character has chosen, or None, if the
        # character.turn() did not return anything that points to an available
        # action.
        return actions.get(player_action)

    def _action_pick_up(self, character: Character, item: Item):
        self.item_storage.remove_item(item.id)
        character.item_storage.add_item(item)

    @property
    def storage_actions(self):
        actions = []

        for item in self.item_storage.get_items():
            actions.append(LambdaAction(f'Examine {item.title}',
                                        lambda story, character:
                                            print(f"You see {item}")))
            actions.append(LambdaAction(f'Pick up {item.title}',
                                        lambda story, character:
                                            self._action_pick_up(character, item)))

        # Exit the item storage node (go back).
        actions.append(GoBackAction("Stop browsing."))

        return actions
