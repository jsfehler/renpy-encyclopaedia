from encyclopaedia import EncEntry


def test_str():
    e = EncEntry(
        number=1,
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    assert "01: Test Name" == str(e)


def test_str_no_number():
    e = EncEntry(
        name="Test Name",
        text=["Test Text"],
        locked=False,
    )

    assert "None: Test Name" == str(e)
