from unittest.mock import patch

from encyclopaedia import Encyclopaedia
from encyclopaedia import EncEntry
from encyclopaedia.hyperlink_ren import set_encentry_from_text_anchor


@patch("encyclopaedia.hyperlink_ren.store")
def test_set_encentry_from_text_anchor(mock):
    enc = Encyclopaedia()

    e = EncEntry(
        parent=enc,
        number=4,
        name="Apple",
        text=["Test Text"],
    )

    # Immitate renpy.store
    mock.enc = enc
    mock.e = e

    set_encentry_from_text_anchor("enc->e")

    assert enc.active == e
