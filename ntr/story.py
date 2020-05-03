from .utils import sp


def story_factory(story_data):
    story_description = story_data['info']['description']
    story_start = story_data['info']['start']
    story_map = story_data['map']

    return Story(story_description, story_start, story_map)


class Story(object):
    """A story object."""

    _description = ""
    _start = None
    _game_map = {}

    def __init__(self, description, start, game_map):
        self._description = description
        self._start = start
        self._game_map = game_map

    def run(self):
        current_place = self._start

        while True:
            self._show_place_text(current_place)
            current_place = self._handle_place_options(current_place)

            if current_place is None:
                break

    def _show_place_text(self, place_id):
        place_text = self._game_map[place_id]['text']
        if type(place_text) == list:
            for line in place_text:
                sp(line)
        else:
            sp(place_text)

    def _handle_place_options(self, place_id):
        keys = {}  # Mapping of "option key" -> "next place ID"
        options = self._game_map[place_id].get('options', None)

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
