import sys
from typing import Callable

import pytest

from mock_renpy import renpy

sys.modules['renpy'] = renpy

from renpy.game import MockPersistent, persistent  # NOQA

from encyclopaedia import EncEntry, Encyclopaedia  # NOQA


@pytest.fixture
def add_dummy_entries() -> Callable[['Encyclopaedia', int, bool], list['EncEntry']]:
    """Quickly fill an Encyclopaedia up."""
    def _factory(
        enc: 'Encyclopaedia',
        amount: int,
        *args,
        **kwargs,
    ) -> list['EncEntry']:
        rv = []

        for x in range(amount):
            entry = EncEntry(
                parent=enc,
                name=f"Zeus_{str(x)}",
                text=["Dummy Text"],
                *args,
                **kwargs,
            )
            rv.append(entry)

        return rv

    return _factory


@pytest.fixture(autouse=True)
def cleanup():
    """Reset persistent."""
    renpy.game.persistent = MockPersistent()
