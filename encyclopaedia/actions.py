import renpy.exports as renpy


class EncyclopaediaEntryAction(renpy.ui.Action):
    """
    Action that acts using a specific Encyclopaedia Entry.
    This class is inherited by other Encyclopaedia Actions.
    """
    def __init__(self, encyclopaedia, entry):
        self.enc = encyclopaedia
        self.entry = entry


class SetEntryAction(EncyclopaediaEntryAction):
    """
    Set the selected Encyclopaedia entry into the displaying frame.
    """
    def __call__(self):
        # When setting an entry, index all_entries with the entry.
        # That position is what the Encyclopaedia's active entry should be.
        if self.enc.show_locked_entry is False:
            target_position = self.enc.unlocked_entries.index(self.entry)
        else:
            target_position = self.enc.all_entries.index(self.entry)
        # The active entry is set to whichever list position was found
        self.enc.active = self.entry

        # If an entry was not locked, then it's been viewed, so change
        # the status variable.
        if self.enc.active.locked is False:
            self.enc.active.status = True

        # The current position is updated
        self.enc.current_position = target_position

        renpy.show_screen(self.enc.entry_screen)
        renpy.restart_interaction()


class ChangeEntryAction(renpy.ui.Action):
    """
    Scroll through the entries.
    Used by an Encyclopaedia's PreviousEntry and NextEntry functions.
    """
    def __init__(self, encyclopaedia, direction, block):
        self.enc = encyclopaedia

        # If the button is active or not
        self.block = block

        # Determines if it's going to the previous or next entry
        self.dir = direction

    def get_target_position(self):
        """
        If NOT showing locked entries, the next entry we want to see is
        the next entry in unlocked_entries.
        Else, the next entry we want is the next entry in all_entries.
        """
        if self.enc.show_locked_entry is False:
            target = self.enc.unlocked_entries[self.enc.current_position]
        else:
            target = self.enc.all_entries[self.enc.current_position]

        return target

    def __call__(self):
        if self.block is False:
            # Update the current position
            self.enc.current_position += self.dir

            target_position = self.get_target_position()

            # Update the active entry
            self.enc.active = target_position

            # Mark the entry as viewed, if it's not locked
            if self.enc.active.locked is False:
                self.enc.active.status = True

            # When changing an entry, the sub-entry page number is set back to 1
            self.enc.sub_current_position = 1
            self.enc.active.current_page = self.enc.sub_current_position
            renpy.restart_interaction()

    def get_sensitive(self):
        """
        Determines if the button should be alive or not.

        If at the first entry, block "Previous" button.
        If at the last entry, block "Next" button.
        """
        if self.block:
            return False
        return True


class ChangePageAction(ChangeEntryAction):
    """
    Change the current sub-entry being viewed.
    """
    def __init__(
            self,
            encyclopaedia,
            direction,
            direction2,
            block):
        super(ChangePageAction, self).__init__(
            encyclopaedia,
            direction,
            block,
        )

        self.dir1 = direction
        self.dir2 = direction2

    def __call__(self):
        if self.block is False:
            self.enc.sub_current_position += self.dir2

            self.enc.active.current_page = self.enc.sub_current_position

            renpy.restart_interaction()


class SortEncyclopaedia(renpy.ui.Action):
    """
    Sorts the entries based on sorting_mode.
    """
    def __init__(self, encyclopaedia, sorting_mode=0):
        self.enc = encyclopaedia
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


class SaveStatusAction(renpy.ui.Action):
    """
    Saves the status variable of every entry in an Encyclopaedia inside
    a dictionary.

    Only necessary if using Persistent Data/the Encyclopaedia is save-game
    independent.

    Parameters:
        encyclopaedia: The Encyclopaedia that needs entry statues saved
        status_dictionary: The dictionary that contains all the persistent
            variables.
        key_string: The key for the dictionary, minus the number at the end.

    """
    def __init__(self, encyclopaedia, status_dictionary, key_string):
        self.enc = encyclopaedia
        self.status_dictionary = status_dictionary
        self.key_string = key_string

    def __call__(self):
        for number, item in enumerate(self.enc.all_entries):
            key = self.key_string + str(number)
            self.status_dictionary[key] = item.status


class ResetSubPageAction(renpy.ui.Action):
    """
    Resets the sub-page count to 1. Used when closing the entry screen.
    """
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia

    def __call__(self):
        self.enc.sub_current_position = 1
        self.enc.active.current_page = 1
        renpy.restart_interaction()


class ToggleShowLockedButtonsAction(renpy.ui.Action):
    """
    Toggles if locked Entries will be shown in the list of Entries or not.
    For the sake of User Experience, this is best left as a debug option.
    """
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia

    def __call__(self):
        self.enc.show_locked_buttons = not self.enc.show_locked_buttons
        renpy.restart_interaction()


class ToggleShowLockedEntryAction(renpy.ui.Action):
    """
    Toggles if locked Entries can be viewed or not.
    For the sake of User Experience, this is best left as a debug option.
    """
    def __init__(self, encyclopaedia):
        self.enc = encyclopaedia

    def __call__(self):
        self.enc.show_locked_entry = not self.enc.show_locked_entry
        renpy.restart_interaction()
