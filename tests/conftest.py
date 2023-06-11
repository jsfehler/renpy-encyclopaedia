import sys

import pytest

from encyclopaedia import EncEntry

from mock_renpy import renpy

sys.modules['renpy'] = renpy


@pytest.fixture
def add_dummy_entries():
    """Quickly fill an Encyclopaedia up."""
    def func(enc, amount, locked: bool = False) -> list["EncEntry"]:
        rv = []

        for x in range(amount):
            entry = EncEntry(
                parent=enc,
                name=f"Dummy Name {str(x)}",
                text=["Dummy Text"],
                locked=True,
            )
            rv.append(entry)

    return func
