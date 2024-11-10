from encyclopaedia import EncEntry, Encyclopaedia


def test_name_set():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    # Pretend we viewed the entry
    e.viewed = True

    e.name = "Another Name"

    assert e.viewed is False


def test_text_set():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    # Pretend we viewed the entry
    e.viewed = True

    e.text = ["New Text"]

    assert e.viewed is False
