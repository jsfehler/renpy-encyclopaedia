from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry


def test_image():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        image="placeholder",
        locked_image="placeholder"
    )

    assert "placeholder" == e.image
    assert e.has_image


def test_unlock_entry():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=True,

    )

    assert e in enc.all_entries
    assert e not in enc.unlocked_entries

    # Unlock the first entry
    e.locked = False
    assert e.locked is False

    assert e in enc.all_entries
    assert e in enc.unlocked_entries


def test_add_subpage():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False
    )

    ee = EncEntry(
        parent=e,
        name="A Sub-Page",
        text=["Test Text"],
        locked=False
    )

    assert [[1, e], [2, ee]] == e.sub_entry_list


def test_unlock_subpage():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    ee = EncEntry(
        parent=e,
        name="A Sub-Page",
        text=["Test Text"],
        locked=True
    )

    # Unlock the sub-page
    ee.locked = False
    assert ee.locked is False


def test_label():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    assert "01: Test Name" == e.label


def test_name():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    assert "Test Name" == e.name


def test_name_locked():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=True,
    )

    assert "???" == e.name


def test_text_locked():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=True,
    )

    assert ["???"] == e.text
