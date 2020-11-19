from ntr.utils import sp
from ntr.items import ItemStorage


class Character:
    hp = 100
    item_storage = None

    def __init__(self) -> None:
        self.item_storage = ItemStorage()

    def turn(self):
        raise NotImplementedError


class Player(Character):
    def turn(self, decision: 'ntr.gameplay.Decision'):
        sp(decision.description)
        sp()
        sp("Your options:")
        for key, label in decision.get_labeled_options().items():
            sp(f"{key}/ {label}")

        sp()
        return input('>>>')

    def _print_place_text(self, current_place: 'ntr.story.PlaceNode'):
        if place_items:
            sp('There are: ' if len(place_items) > 1 else 'There is: ', end='')
            for item in place_items:
                sp(item.title)
