#!/usr/bin/env python

import os
import neon

from ntr.utils import sp, get_sys_arg
from ntr.story import Story, story_factory


def main():
    story_file_path = get_sys_arg(1)

    if not story_file_path:
        sp("Story file not provided.")
        return

    elif not os.path.isfile(story_file_path):
        sp(f"File '{story_file_path}' not found.")
        return

    sp(f"Loading story file {story_file_path} ...")

    with open(story_file_path, "r") as file:
        try:
            story_data = neon.decode(file.read())
        except Exception:
            sp("Invalid story file format.")
            return

    story = story_factory(story_data)
    story.run()

try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    print("Byee")
