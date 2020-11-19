import sys
import time
from json import loads, dumps

DEBUG_MODE = True


def split_iter(items, batch_size):
    """Yields smaller iterators from a collection/iterator, each containing
    specified number of sequential items from the original collection/iterator.
    """
    if batch_size < 1:
        raise ValueError("Batch size too low.")

    counter = 0
    collector = []
    it = iter(items)

    while True:
        counter += 1

        try:
            collector.append(it.__next__())
        except StopIteration:
            yield collector
            break

        if counter < batch_size:
            continue

        yield collector
        collector.clear()
        counter = 0


def sp(text: str = '', end='\n'):
    """Primary text renderer function - with a pretty "scanning" effect."""
    if DEBUG_MODE:
        print(text, end=end)
        return

    for batch in split_iter(text, 2):
        print(''.join(batch), end="", flush=True)
        time.sleep(0.01)

    # Put a newline at the end.
    print(end=end)


def get_sys_arg(index):
    """Get program's argument by its index, or return an empty string."""
    try:
        return sys.argv[index]
    except IndexError:
        return ''


def normalize_dict(ordered_dict):
    return loads(dumps(ordered_dict))
