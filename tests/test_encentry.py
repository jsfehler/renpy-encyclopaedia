from encyclopaedia.encyclopaedia import Encyclopaedia
from encyclopaedia.encentry import EncEntry

from renpy.game import persistent


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
        locked=True,
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


def test_locked_persistent_get():
    """When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    about_zeus = EncEntry(
        parent=enc,
        name="Zeus",
        text=["Test Text"],
        locked=True,
        locked_persistent=True,
    )

    assert about_zeus.locked == persistent.Zeus_locked


def test_locked_persistent_set():
    """When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    about_zeus = EncEntry(
        parent=enc,
        name="Zeus",
        text=["Test Text"],
        locked=True,
        locked_persistent=True,
    )

    about_zeus.locked = False

    assert persistent.Zeus_locked is False
    assert about_zeus.locked == persistent.Zeus_locked


def test_viewed_persistent_get():
    """When viewed status is controlled by a persistent variable
    Then the EncEntry's viewed attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    about_zeus = EncEntry(
        parent=enc,
        name="Zeus",
        text=["Test Text"],
        viewed_persistent=True,
    )

    assert about_zeus.viewed == persistent.Zeus_viewed


def test_viewed_persistent_set():
    """When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    about_zeus = EncEntry(
        parent=enc,
        name="Zeus",
        text=["Test Text"],
        viewed_persistent=True,
    )

    about_zeus.viewed = True

    assert persistent.Zeus_viewed is True
    assert about_zeus.viewed == persistent.Zeus_viewed
