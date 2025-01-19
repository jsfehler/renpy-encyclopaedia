from renpy import store

from .encentry_ren import EncEntry
from .encyclopaedia_ren import Encyclopaedia

"""renpy
init -83 python:
"""

from typing import Optional, Union  # NOQA E402


class AchievementEncEntry(EncEntry):
    """EncEntry which uses Ren'Py's achievement system to manage locked state.

    Args:
        achievement: The name of the achievement
        parent: The parent container for the EncEntry.
        number: The entry's number.
            If this is not set then it will be given a number automatically.
        name: Title, normally used for buttons and headings.
        text: The text to be displayed when the entry is viewed.
        subject: The subject to associate the entry with.
            Used for sorting and filtering.
        viewed: Set the viewed status of the EncEntry. Default is False.
            Only use if the Encyclopaedia is save-game independent.
        viewed_persistent: Use persistent data for recording viewed status.
        image: The image displayed with the Entry text. Default is None.
        locked_name: Placeholder text for the name. Shown when the entry is locked.
        locked_text: Placeholder text for the text. Shown when the entry is locked.
        locked_image: Placeholder image for the image. Shown when the entry is locked.
        locked_image_tint: If no specific locked image is provided,
            a tinted version of the image will be used.
            The amount of tinting can be set with RGB values in a tuple.
    """
    def __init__(
        self,
        achievement: str,
        parent: Optional[Union['Encyclopaedia', 'EncEntry']] = None,
        number: Optional[int] = None,
        name: str = "",
        text: Union[str, list[str]] = "",
        subject: str = "",
        viewed: bool = False,
        viewed_persistent: Optional[bool] = False,
        image: Optional[str] = None,
        locked_name: str = "???",
        locked_text: str = "???",
        locked_image: Optional[str] = None,
        locked_image_tint: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> None:
        self.achievement = achievement

        super().__init__(
            parent=parent,
            number=number,
            name=name,
            text=text,
            subject=subject,
            viewed=viewed,
            viewed_persistent=viewed_persistent,
            image=image,
            locked_name=locked_name,
            locked_text=locked_text,
            locked_image=locked_image,
            locked_image_tint=locked_image_tint,
        )

    @property
    def locked(self) -> bool:
        """If the achievement is granted, consider the Entry unlocked."""
        granted = store.achievement.has(self.achievement)

        if granted and (self.parent is not None):
            if isinstance(self.parent, Encyclopaedia):
                unlocked = self.parent.unlocked_entries
            else:
                unlocked = self.parent.unlocked_pages

            if self not in unlocked:
                self.parent._add_entry_to_unlocked_entries(self)

        return not granted

    @locked.setter
    def locked(self, new_value: bool) -> None:
        """AchievementEncEntry cannot modify the locked attribute."""
        raise AttributeError("'locked' status cannot be manually modified.")
