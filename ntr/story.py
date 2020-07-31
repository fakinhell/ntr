from .utils import sp


class Story(object):
    """Class representing a story."""
    _description_text = ""
    _start = None
    _map = {}

    def __init__(self, description_text, start, game_map):
        self._description_text = description_text
        self._start = start
        self._map = game_map

    def run(self):
        current_place = self._start

        while True:
            self._print_place_text(current_place)
            current_place = self._handle_place_options(current_place)

            if current_place is None:
                break

    def _print_place_text(self, place_id):
        place_text = self._map[place_id]['text']
        if type(place_text) == list:
            for line in place_text:
                sp(line)
        else:
            sp(place_text)

        print()

    def _handle_place_options(self, place_id):
        keys = {}  # Helper mapping of "option key" -> "next place ID"
        options = self._map[place_id].get('options', None)

        if not options:
            return None

        indent = "Your options:"
        for key, option in options.items():
            keys[key] = option['goto']
            sp(f"{indent} {key}/ {option['label']}")
            indent = "             "

        # Bother our user until a valid option is selected.
        while True:
            pressed = input(">>> ")

            if pressed in keys.keys():
                break

            sp("Enter a valid option.")

        return keys[pressed]
