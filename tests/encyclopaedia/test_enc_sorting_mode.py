from encyclopaedia import EncEntry, Encyclopaedia, constants_ren


def test_reverse_alphabetical_sorting():
    enc = Encyclopaedia(sorting_mode=constants_ren.SortMode.REVERSE_ALPHABETICAL)

    apple = EncEntry(
        parent=enc,
        name="Apple",
        text=[""],
    )

    banana = EncEntry(
        parent=enc,
        name="Banana",
        text=[""],
    )

    cantaloupe = EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=[""],
    )

    assert [cantaloupe, banana, apple] == enc.all_entries


def test_subject_sorting():
    enc = Encyclopaedia(sorting_mode=constants_ren.SortMode.SUBJECT)

    asparagus = EncEntry(
        parent=enc,
        name="Asparagus",
        text=[""],
        subject="Vegetable",
    )

    apple = EncEntry(
        parent=enc,
        name="Apple",
        text=[""],
        subject="Fruit",
    )

    banana = EncEntry(
        parent=enc,
        name="Banana",
        text=[""],
        subject="Fruit",
    )

    cantaloupe = EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=[""],
        subject="Fruit",
    )

    assert [apple, banana, cantaloupe, asparagus] == enc.all_entries


def test_encyclopaedia_property_reverse_sorting():
    enc = Encyclopaedia()

    EncEntry(
        parent=enc,
        name="Apple",
        text=[""],
    )

    EncEntry(
        parent=enc,
        name="Banana",
        text=[""],
    )

    EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=[""],
    )

    enc.sort(mode=constants_ren.SortMode.NUMBER, reverse=True)
    assert enc.reverse_sorting is True

    enc.sort(mode=constants_ren.SortMode.NUMBER, reverse=False)
    assert enc.reverse_sorting is False


def test_encyclopaedia_sort_alphabetical_reversed():
    """SortMode.ALPHABETICAL + reverse is the equivalent of SortMode.REVERSE_ALPHABETICAL"""
    enc = Encyclopaedia()

    apple = EncEntry(
        parent=enc,
        name="Apple",
        text=[""],
    )

    banana = EncEntry(
        parent=enc,
        name="Banana",
        text=[""],
    )

    cantaloupe = EncEntry(
        parent=enc,
        name="Cantaloupe",
        text=[""],
    )

    enc.sort(mode=constants_ren.SortMode.ALPHABETICAL, reverse=True)

    assert [cantaloupe, banana, apple] == enc.current_entries
