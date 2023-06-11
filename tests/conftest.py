import sys
from typing import Callable

import pytest

from mock_renpy import renpy

sys.modules['renpy'] = renpy

from encyclopaedia import Encyclopaedia, EncEntry  # NOQA


@pytest.fixture
def add_dummy_entries() -> Callable[['Encyclopaedia', int, bool], list['EncEntry']]:
    """Quickly fill an Encyclopaedia up."""
    def func(
        enc: 'Encyclopaedia',
        amount: int,
        locked: bool = False,
    ) -> list['EncEntry']:
        rv = []

        for x in range(amount):
            entry = EncEntry(
                parent=enc,
                name=f"Dummy Name {str(x)}",
                text=["Dummy Text"],
                locked=locked,
            )
            rv.append(entry)

        return rv

    return func
