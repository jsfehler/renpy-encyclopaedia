from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry
from encyclopaedia import EncEntryTemplate

import pytest


def test_encentry_template():
    enc = Encyclopaedia()

    GreekGodsEntry = EncEntryTemplate(subject="Greek Gods")  # NOQA: N806

    about_zeus = GreekGodsEntry(parent=enc, name="Zeus")

    assert isinstance(about_zeus, EncEntry)
    assert "Greek Gods" == about_zeus.subject


def test_encentry_template_invalid_args():
    """Arguments that aren't valid for an EncEntry aren't valid here."""
    enc = Encyclopaedia()

    GreekGodsEntry = EncEntryTemplate(food="Pizza")  # NOQA: N806

    with pytest.raises(TypeError):
        GreekGodsEntry(parent=enc, name="Zeus")
