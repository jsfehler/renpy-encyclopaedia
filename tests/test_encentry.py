import pytest

from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry

from renpy.game import persistent


def test_image():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        image="placeholder",
        locked_image="placeholder",
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


def test_add_page():
    """
    When an EncEntry has another EncEntry as a parent
    Then it becomes a page of the parent EncEntry.
    """
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
        locked=False,
    )

    assert [e, ee] == e.pages


def test_add_page_correct_number():
    """
    When an Encyclopaedia has multiple EncEntry
    And each EncEntry has multiple pages
    And there are multiple EncEntry in the Encyclopaedia
    Then the page number of each page in the EncEntry is tracked correctly
    """
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="E1",
        text=["Test Text"],
        locked=False,
    )

    ee = EncEntry(
        parent=e,
        name="E2",
        text=["Test Text"],
        locked=False,
    )

    eee = EncEntry(
        parent=e,
        name="E3",
        text=["Test Text"],
        locked=False,
    )

    f = EncEntry(
        parent=enc,
        name="F1",
        text=["Test Text"],
        locked=False,
    )

    ff = EncEntry(
        parent=f,
        name="F2",
        text=["Test Text"],
        locked=False,
    )

    fff = EncEntry(
        parent=f,
        name="F3",
        text=["Test Text"],
        locked=False,
    )

    assert e.number == 1
    assert f.number == 2

    assert e.page_number == 1
    assert ee.page_number == 2
    assert eee.page_number == 3

    assert f.page_number == 1
    assert ff.page_number == 2
    assert fff.page_number == 3


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

    assert ee in e.pages

def test_label():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    assert "01: Test Name" == e.label


def test_label_no_number():
    e = EncEntry(
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    assert "None: Test Name" == e.label


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


def test_text_modify():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    # Pretend we viewed the entry
    e.viewed = True

    # Modify text
    e.text = ["New Text"]

    assert e.viewed is False


def test_image_add():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    # Ensure EncEntry knows it has no image
    e.has_image = False

    # Pretend we viewed the entry
    e.viewed = True

    # Add image
    e.image = "foobar"

    assert e.has_image
    assert e.viewed is False


def test_locked_persistent_first_get(add_dummy_entries):
    """When locked status is controlled by a persistent variable
    Then the persistent variable is set to the value of the locked attribute
    And the EncEntry's locked variable is set to the value of the locked attribute
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        locked=False,
        locked_persistent=True,
    )

    assert result[0].locked is False
    assert persistent.Zeus_0_locked is False


def test_locked_persistent_get(add_dummy_entries):
    """When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        locked=True,
        locked_persistent=True,
    )

    assert result[0].locked == persistent.Zeus_0_locked


def test_locked_persistent_set(add_dummy_entries):
    """When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        locked=True,
        locked_persistent=True,
    )

    result[0].locked = False

    assert persistent.Zeus_0_locked is False
    assert result[0].locked == persistent.Zeus_0_locked


def test_viewed_persistent_get(add_dummy_entries):
    """When viewed status is controlled by a persistent variable
    Then the EncEntry's viewed attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        viewed_persistent=True,
    )

    assert result[0].viewed == persistent.Zeus_0_viewed


def test_viewed_persistent_set(add_dummy_entries):
    """When locked status is controlled by a persistent variable
    Then the EncEntry's locked attribute should be linked to a persistent
    variable.
    """
    enc = Encyclopaedia()

    result = add_dummy_entries(
        enc=enc,
        amount=1,
        viewed_persistent=True,
    )

    result[0].viewed = True

    assert persistent.Zeus_0_viewed is True
    assert result[0].viewed == persistent.Zeus_0_viewed


def test_word_count():
    """When checking the word count of an EncEntry,
    Then the number returned is correct.
    """
    enc = Encyclopaedia()

    about_zeus = EncEntry(
        parent=enc,
        name="Zeus",
        text=["Test Text To Check Word Count"],
    )

    assert 6 == about_zeus.word_count


def test_repr():
    enc = Encyclopaedia(name="Dummy Enc Name")

    e = EncEntry(parent=enc, name="Dummy EncEntry", text="Dummy Text")

    assert repr(e) == "EncEntry(number=1, name=Dummy EncEntry)"


def test_add_entry_already_in_page():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"],
    )

    ee = EncEntry(
        parent=enc,
        name="Test Page",
        text=["Test Text"],
    )

    with pytest.raises(ValueError):
        e.add_entry(ee)
