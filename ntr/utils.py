import time


def sp(text):
    """Primary text renderer function - with a pretty "scanning" effect."""
    for c in text:
        print(c, end="", flush=True)
        time.sleep(0.01)

    # Newline at the end.
    print()
