from ntr.inventory import Item, Inventory


def test_items():
    i_a = Item("paradox")
    i_b = Item("paradox")
    i_c = Item("radiation")

    assert i_a is not i_b
    assert i_a.id != i_b.id
    assert i_a.title == i_b.title

    assert i_a is not i_c
    assert i_a.id != i_c.id
    assert i_a.title != i_c.title


def test_inventory():
    i_a = Item("paradox")
    i_b = Item("radiation")

    base = [i_a, i_b]
    inv = Inventory(base)

    _ = inv.get_items()
    assert len(_) == 2
    assert set(_.values()) == {i_a, i_b}

    inv.remove_item(i_a.id)
    _ = inv.get_items()
    assert len(_) == 1
    assert set(_.values()) == {i_b}

    i_new = Item("wow, said wilson")
    inv.add_item(i_new)
    _ = inv.get_items()
    assert len(_) == 2
    assert set(_.values()) == {i_b, i_new}

    #
    # Finding items based on some condition.
    #

    found = inv.find_item(lambda item: "wilson" in item.title)
    assert found is i_new

    found = inv.find_item(lambda item: item.title.startswith("wow"))
    assert found is i_new

    found = inv.find_item(lambda item: item.title.startswith("rad"))
    assert found is i_b

    # This will always return nothing.
    found = inv.find_item(lambda item: False)
    assert found is None

    #
    # Deleting all items from inventory.
    #

    inv.delete_all_items()
    assert len(inv.get_items()) == 0
