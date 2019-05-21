#!/usr/bin/env python

import sys
import neon

from os import path

from ntr.utils import sp
from ntr.story import Story


def get_arg(index):
    """Get program's argument by its index, or return an empty string."""
    try:
        sys.argv[index]
    except IndexError:
        return ''
    else:
        return sys.argv[index]


def main():
    story_file_path = get_arg(1)

    if not story_file_path:
        sp("Story file not provided.")
        return

    elif not path.isfile(story_file_path):
        sp(f"File '{story_file_path}' not found.")
        return

    sp(f"Loading story file {story_file_path} ...")

    with open(story_file_path, "r") as file:
        try:
            story_data = neon.decode(file.read())
        except Exception:
            sp("There was an error when decoding story file.")
            return


if __name__ == '__main__':
    main()
