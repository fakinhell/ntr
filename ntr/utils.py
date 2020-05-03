import sys
import time
import itertools


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
        except StopIteration as e:
            yield collector
            break

        if counter < batch_size:
            continue

        yield collector
        collector.clear()
        counter = 0


def sp(text):
    """Primary text renderer function - with a pretty "scanning" effect."""
    for batch in split_iter(text, 2):
        print(''.join(batch), end="", flush=True)
        time.sleep(0.01)

    # Put a newline at the end.
    print()


def get_sys_arg(index):
    """Get program's argument by its index, or return an empty string."""
    try:
        return sys.argv[index]
    except IndexError:
        return ''
