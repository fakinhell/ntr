#!/usr/bin/env python

import sys
from os import path

from ntr.utils import sp


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

    sp(f"File {story_file_path} found! YEAH.")


if __name__ == '__main__':
    main()
test doprdele