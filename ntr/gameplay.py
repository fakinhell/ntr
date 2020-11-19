from ntr.utils import sp, normalize_dict
from ntr.story import World, Story, PlaceNode
from ntr.characters import Player


class Decision:
    description = ''
    options = None

    def __init__(self, description: str, options: None):
        self.description = description
        self.options = options

    def get_labeled_options(self):
        return {k: o.label for k, o in self.options.items()}

    def is_valid_option(self, option) -> bool:
        return option in self.options


class DecisionResult:
    TYPE_GOTO = 1
    TYPE_BROWSE_ITEMS = 2

    TYPE = None
    label = ''

    def __init__(self, label) -> None:
        self.label = label


class GotoDecisionResult(DecisionResult):
    TYPE = DecisionResult.TYPE_GOTO
    goto = None

    def __init__(self, label, goto) -> None:
        super().__init__(label)
        self.goto = goto


class BrowseItemsDecisionResult(DecisionResult):
    TYPE = DecisionResult.TYPE_BROWSE_ITEMS


class GameplayFactory:

    @classmethod
    def build(cls, story: Story) -> 'Gameplay':
        story._map = {k: v for k, v in map(cls._build_place_node,
                      story._map.items())}
        return Gameplay(story)

    @staticmethod
    def _build_place_node(node_tuple):
        node_id = node_tuple[0]
        node_info = node_tuple[1]

        text = node_info.get('text', '')
        text = '\n'.join(text) if isinstance(text, list) else text
        options = list(normalize_dict(node_info.get('options', {})).values())

        return node_id, PlaceNode(node_id=node_id, text=text, options=options)


class Gameplay:
    _story = None
    _world = None

    def __init__(self, story: Story) -> None:
        self._story = story
        self._world = World(story._map)

    def run(self):
        current_node_id = last_node_id = self._story._start
        next_node_id = None
        player = Player()

        while True:
            current_node = self._world._map[current_node_id]

            options = self._build_node_options(current_node)
            decision = Decision(current_node.text, options)
            chosen = options.get(player.turn(decision))

            if isinstance(chosen, GotoDecisionResult):
                next_node_id = chosen.goto
                if next_node_id == '@back':
                    current_node_id = last_node_id
                    continue

            if isinstance(chosen, BrowseItemsDecisionResult):
                interaction = ItemStorageInteraction(current_node.item_storage)
                interaction.run(player)

            if current_node_id is None:
                break

            if next_node_id:
                last_node_id = current_node_id
                current_node_id = next_node_id


    def _build_node_options(self, current_place):
        result = {}
        key_code = ord('a')

        for opt in current_place.options:
            result[chr(key_code)] = GotoDecisionResult(opt['label'],
                                                       opt['goto'])
            key_code += 1

        if current_place.item_storage:
            result['items'] = BrowseItemsDecisionResult('Browse items')

        return result


class PlayerInteraction:
    def run(self, options):
        sp("Your interactions:")

        for interaction_key, option in options.items():
            sp(f"{interaction_key}. {option['text']}")

        while True:
            pressed = input("Interaction >>> ")
            if pressed in options:
                break

            sp("Enter a valid option.")

        return pressed


class ItemStorageInteraction(PlayerInteraction):
    SUBACTION_TYPE_EXAMINE = 'examine'
    SUBACTION_TYPE_PICKUP = 'pick_up'

    def __init__(self, item_storage) -> None:
        self.item_storage = item_storage

    def run(self, player):
        options = {}
        subaction_id = 0

        for item in self.item_storage.get_items():
            subaction_id += 1
            options[str(subaction_id)] = {
                'type': self.SUBACTION_TYPE_EXAMINE,
                'text': f'Examine {item.title}',
                'item': item
            }
            subaction_id += 1
            options[str(subaction_id)] = {
                'type': self.SUBACTION_TYPE_PICKUP,
                'text': f'Pick up {item.title}',
                'item': item
            }

        result = super().run(options)
        subaction = options.get(result)

        if not subaction:
            return

        if subaction['type'] == self.SUBACTION_TYPE_EXAMINE:
            print(f"You see {subaction['item'].title}")

        if subaction['type'] == self.SUBACTION_TYPE_PICKUP:
            player.item_storage.add_item(subaction['item'])
            self.item_storage.remove_item(subaction['item'].id)
            print(f"You picked up {subaction['item'].title}")


