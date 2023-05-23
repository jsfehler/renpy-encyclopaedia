from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry
from encyclopaedia import constants_ren


def test_close_active_entry():
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        name="Test Name",
        text=["Test Text"]
    )

    enc.SetEntry(e)()

    assert enc.active == e

    enc.CloseActiveEntry()()

    assert enc.active is None
