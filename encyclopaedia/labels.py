from typing import TYPE_CHECKING

from .constants import SortMode

from renpy import store

if TYPE_CHECKING:
    from .encyclopaedia import Encyclopaedia


class Labels(store.object):
    """Controls how the labels that display Encyclopaedia data appear.

    Attributes:
        percentage_label (str): Placed next to the percentage unlocked number
        page_label (str): Placed before the entry page displayed
        page_separator_label (str): Placed in-between the
            current page number and the total page number

        sort_number_label (str): Label for Number Sorting
        sort_alphabetical_label (str): Label for Alphabetical sorting
        sort_reverse_alphabetical_label (str): Label for Reverse Alphabetical
            sorting
        sort_subject_label (str): Label for Subject sorting
        sort_unread_label (str): Label for Unread sorting

        unread_entry_label (str): Default for the tag next to unread entries
    """
    def __init__(self, encyclopaedia: 'Encyclopaedia') -> None:
        self.encyclopaedia = encyclopaedia

        self.percentage_label = '%'
        self.page_label = 'Page'
        self.page_separator_label = '/'

        self.sort_number_label = "Number"
        self.sort_alphabetical_label = "A to Z"
        self.sort_reverse_alphabetical_label = "Z to A"
        self.sort_subject_label = "Subject"
        self.sort_unread_label = "Unread"

        self.unread_entry_label = "New!"

    @property
    def percentage_unlocked(self) -> str:
        """Percentage representation of the amount of the encyclopaedia
        that's unlocked. ie: '50%'.

        Returns:
            str
        """
        percentage_unlocked = int(self.encyclopaedia.percentage_unlocked)
        return "{}{}".format(percentage_unlocked, self.percentage_label)

    @property
    def entry_current_page(self) -> str:
        """The sub-page of an entry that is being viewed.

        Returns:
            str
        """
        try:
            total_pages = self.encyclopaedia.active.pages
        except AttributeError:
            raise AttributeError(
                "Cannot display Entry's current page when no entry is open."
            )

        label = "{0} {1} {2} {3}".format(
            self.page_label,
            self.encyclopaedia.sub_current_position,
            self.page_separator_label,
            total_pages
        )

        return label

    @property
    def sorting_mode(self) -> str:
        """Label for the encyclopaedia's current sorting mode.

        Returns:
            str
        """
        enc = self.encyclopaedia

        sorting_strings = {
            SortMode.NUMBER: self.sort_number_label,
            SortMode.ALPHABETICAL: self.sort_alphabetical_label,
            SortMode.REVERSE_ALPHABETICAL: self.sort_reverse_alphabetical_label,  # NOQA: E501
            SortMode.SUBJECT: self.sort_subject_label,
            SortMode.UNREAD: self.sort_unread_label
        }

        return sorting_strings[enc.sorting_mode]
