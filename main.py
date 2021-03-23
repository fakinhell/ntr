#!/usr/bin/env python
import sys
import yaml

from os import path

from ntr.utils import sp
from ntr.gameplay import GameplayFactory, Story


def get_arg(index):
    """Get program's argument by its index, or return an empty string."""
    try:
        return sys.argv[index]
    except IndexError:
        return ''


def main(story_file_path):
    if not story_file_path:
        sp("Story file not provided.")
        return

    elif not path.isfile(story_file_path):
        sp(f"File '{story_file_path}' not found.")
        return

    sp(f"Loading story file {story_file_path} ...")

    with open(story_file_path) as file:
        try:
            story_data = yaml.load(file.read(), Loader=yaml.SafeLoader)
        except Exception:
            sp("There was an error when decoding story file.")
            raise

    story_description = story_data['info']['description']
    start_place_id = story_data['info']['start']
    story_map = story_data['map']

    story = Story(story_description, start_place_id, story_map)
    gameplay = GameplayFactory.build(story)
    gameplay.run()


if __name__ == '__main__':
    story_file_path = get_arg(1)
    main('story.nsfw')
