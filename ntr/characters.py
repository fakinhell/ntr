import ntr

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
    def turn(self, text: str, actions: "ntr.gameplay.Actions"):
        sp(text)
        print()

        sp("Your options:")
        for key, label in actions:
            sp(f"{key}/ {label}")

        sp()
        return input('>>> ')
