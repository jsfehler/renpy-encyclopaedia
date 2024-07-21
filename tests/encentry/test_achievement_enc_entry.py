from unittest.mock import patch

import pytest

from encyclopaedia import Encyclopaedia
from encyclopaedia import AchievementEncEntry


def test_achievement_enc_entry_granted():
    with patch('encyclopaedia.achentry_ren.store.achievement') as mock_ach:

        # The achievement has been granted
        mock_ach.has.return_value = True

        achievments_enc = Encyclopaedia()

        e = AchievementEncEntry(
            parent=achievments_enc,
            achievement="DummyAch",
            name="Test Achievement",
            text=["Test Achievement Text"],
        )

        assert e.locked is False


def test_achievement_enc_entry_not_granted():
    with patch('encyclopaedia.achentry_ren.store.achievement') as mock_ach:

        # The achievement has not been granted
        mock_ach.has.return_value = False

        achievments_enc = Encyclopaedia()

        e = AchievementEncEntry(
            parent=achievments_enc,
            achievement="DummyAch",
            name="Test Achievement",
            text=["Test Achievement Text"],
        )

        assert e.locked


def test_achievement_enc_entry_change_locked():
    with patch('encyclopaedia.achentry_ren.store.achievement') as mock_ach:

        # The achievement has been granted
        mock_ach.has.return_value = True

        achievments_enc = Encyclopaedia()

        e = AchievementEncEntry(
            parent=achievments_enc,
            achievement="DummyAch",
            name="Test Achievement",
            text=["Test Achievement Text"],
        )

        with pytest.raises(AttributeError):
            e.locked = True
