init -1500 python:
    class EncyclopaediaAction(Action):
        """Base Action that requires an Encyclopaedia.

        Args:
            encyclopaedia (Encyclopaedia): The encyclopaedia to use.
        """
        def __init__(self, encyclopaedia):
            self.enc = encyclopaedia


    class SetEntryAction(EncyclopaediaAction):
        """Set the given Encyclopaedia entry as the active entry.

        Used for opening entries directly.

        Attributes:
            entry (EncEntry): The entry to be made active.
        """
        def __init__(self, encyclopaedia, entry):
            super(SetEntryAction, self).__init__(encyclopaedia)

            self.entry = entry

        def __call__(self):
            # Find the position of the entry
            if self.enc.show_locked_entry is False:
                target_position = self.enc.unlocked_entries.index(self.entry)
            else:
                target_position = self.enc.all_entries.index(self.entry)

            # The active entry is set to whichever list position was found.
            self.enc.active = self.entry

            if self.enc.active.locked is False:
                if self.entry.viewed is False:
                    # Run the callback, if provided.
                    if self.entry.viewed_callback is not None:
                        self.entry.viewed_callback[0](self.entry.viewed_callback[1])
                # Mark the entry as viewed.
                self.enc.active.viewed = True

            self.enc.current_position = target_position

            # Show the entry screen associated with the encyclopaedia.
            renpy.show_screen(self.enc.entry_screen, self.enc)
            renpy.restart_interaction()


    class ChangeAction(EncyclopaediaAction):
        """Base Action that swaps one entry or page for another.

        Args:
            block (bool): True if at the first or last entry
        """
        def __init__(self, encyclopaedia, direction, block):
            super(ChangeAction, self).__init__(encyclopaedia)

            # Determines if it's going to the previous or next entry.
            self.direction = direction

            # If the button is active or not.
            self.block = block

        def get_sensitive(self):
            """Determines if the button should be alive or not.

            Returns:
                bool
            """
            if self.block:
                return False
            return True


    class ChangeEntryAction(ChangeAction):
        """Change the current entry being viewed.

        Used for switching from one entry to another.

        Used by an Encyclopaedia's PreviousEntry() and NextEntry() functions.
        """

        def get_entry(self):
            """Get the entry at the given index.

            If NOT showing locked entries, the next entry we want to see is
            the next entry in unlocked_entries.
            Else, the next entry we want is the next entry in all_entries.

            Returns:
                EncEntry
            """
            if self.enc.show_locked_entry is False:
                entry = self.enc.unlocked_entries[self.enc.current_position]
            else:
                entry = self.enc.all_entries[self.enc.current_position]

            return entry

        def __call__(self):
            if self.block is False:
                # Update the current position.
                self.enc.current_position += self.direction

                # Update the active entry.
                self.enc.active = self.get_entry()

                if self.enc.active.locked is False:
                    # Run the callback, if provided.
                    if self.enc.active.viewed_callback is not None:
                        self.enc.active.viewed_callback[0](
                            self.enc.active.viewed_callback[1]
                        )
                    # Mark the entry as viewed.
                    self.enc.active.viewed = True

                # When changing an entry, the current sub-entry page number is
                # set back to 1.
                self.enc.sub_current_position = 1
                self.enc.active.current_page = self.enc.sub_current_position

                renpy.restart_interaction()


    class ChangePageAction(ChangeAction):
        """Change the current sub-entry being viewed.

        Used for switching from one page to another.

        Used by an Encyclopaedia's PreviousPage() and NextPage() functions.
        """
        def __call__(self):
            if self.block is False:
                # The Encyclopaedia's page display changes.
                self.enc.sub_current_position += self.direction

                # The EncEntry's current page changes to match.
                self.enc.active.current_page = self.enc.sub_current_position

                if self.enc.active.current_page.viewed is False:
                    self.enc.active.current_page.viewed = True

                renpy.restart_interaction()


    class SortEncyclopaedia(EncyclopaediaAction):
        """Sorts the entries based on encyclopaedia.sorting_mode.
        """
        def __init__(self, encyclopaedia, sorting_mode=0):
            super(SortEncyclopaedia, self).__init__(encyclopaedia)

            self.sorting_mode = sorting_mode

            self.reverse = False
            if sorting_mode == self.enc.SORT_REVERSE_ALPHABETICAL:
                self.reverse = True

        def __call__(self):
            self.enc.sort_entries(
                sorting=self.sorting_mode,
                reverse=self.reverse
            )

            self.enc.sorting_mode = self.sorting_mode
            renpy.restart_interaction()


    def _build_subject_filter(enc, subject):
        """Build an encyclopaedia's filtered_entries based on the subject given.

        Args:
            enc (Encyclopaedia): The encyclopaedia to filter.
            subject (str): The subject for the filter.
        """
        if enc.show_locked_buttons is False:
            entries = enc.unlocked_entries
        else:
            entries = enc.all_entries

        enc.filtered_entries = [i for i in entries if i.subject == subject]


    class FilterBySubject(EncyclopaediaAction):
        """Create a filter for entries, based on the given subject.
        """
        def __init__(self, encyclopaedia, subject):
            super(FilterBySubject, self).__init__(encyclopaedia)

            self.subject = subject

        def __call__(self):
            self.enc.filtering = self.subject

            _build_subject_filter(self.enc, self.subject)

            renpy.restart_interaction()


    class ClearFilter(EncyclopaediaAction):
        """Stop filtering an Encyclopaedia.
        """
        def __call__(self):
            self.enc.filtering = False
            renpy.restart_interaction()


    class ResetSubPageAction(EncyclopaediaAction):
        """Resets the sub-page count to 1. Used when closing the entry screen.
        """
        def __call__(self):
            self.enc.sub_current_position = 1
            self.enc.active.current_page = 1
            renpy.restart_interaction()


    class ToggleShowLockedButtonsAction(EncyclopaediaAction):
        """Toggles if locked Entries will be visible in the list of Entries.
        """
        def __call__(self):
            self.enc.show_locked_buttons = not self.enc.show_locked_buttons

            # Ensure the filtering isn't broken by hiding buttons.
            if self.enc.filtering:
                _build_subject_filter(self.enc, self.enc.filtering)

            # Ensure the sorting isn't broken by hiding buttons.
            reverse = False
            if self.enc.sorting_mode == self.enc.SORT_REVERSE_ALPHABETICAL:
                reverse = True

            self.enc.sort_entries(sorting=self.enc.sorting_mode, reverse=reverse)

            renpy.restart_interaction()


    class ToggleShowLockedEntryAction(EncyclopaediaAction):
        """Toggles if locked Entries can be viewed.
        """
        def __call__(self):
            self.enc.show_locked_entry = not self.enc.show_locked_entry
            renpy.restart_interaction()
