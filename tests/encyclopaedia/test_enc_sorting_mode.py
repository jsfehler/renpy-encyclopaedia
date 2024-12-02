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
