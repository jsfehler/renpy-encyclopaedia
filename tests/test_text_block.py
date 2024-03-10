from encyclopaedia.text_block_ren import text_block


def test_text_block():
    """
    When a string is wrapped by text_block
    Then whitespace padding is removed
    And newliness are removed
    And blank lines are preserved
    """
    result = text_block("""\
    Test 1
    Test 2

    Test 3
    """
    )

    assert result == "Test 1 Test 2\n\nTest 3 "
