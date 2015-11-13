import copy


class EntryList(list):
    """
    list that's been extended with specific sorting options.
    EntryList should only contain EncEntry objects.
    """
    @staticmethod
    def _push_to_bottom(list_instance, item):
        """
        Take a list and an item in that list. 
        Pop the item from the list and insert it at the bottom.
        
        Parameters:
            list_instance (EntryList): The list to use
            item (EncEntry): The item to push to the bottom
        
        Returns:
            EntryList
        """
        list_length = len(list_instance)
        popped = list_instance.pop(list_instance.index(item))
        list_instance.insert(list_length, popped)
        
        return list_instance
        
    def _send_locked_entries_to_bottom(self):
        """
        Moves all the locked entries to the bottom of the list.

        Returns:
            self
        """
        # We can't pop and insert directly; the loop will get screwed up.   
        changed_list = copy.copy(self)

        # Loop over the list, but do the changes to changed_all_entries
        for item in self:
            if item.locked is not False:
                changed_list = self._push_to_bottom(
                    changed_list,
                    item
                )
        
        del self[:]
        for item in changed_list:
            self.append(item)        
        
        return self

    @staticmethod
    def _get_number_key(item):
        """
        Returns:
            Key for sorting by number
        """
        return item.number
        
    def sort_by_number(self):
        """
        Sorts entries by their number.
        """
        self.sort(key=self._get_number_key)
        return self

    @staticmethod
    def _get_name_key(item):
        """
        Returns:
            Key for sorting by name
        """
        return item.name
        
    def sort_by_name(self, reverse=False, locked_at_bottom=True):
        """
        Sorts entries by their name attribute.

        Parameters:
            reverse (bool): False for A to Z, True for Z to A
            locked_at_bottom (bool): Locked entries go to the bottom of the list

        Returns:
            self
        """
        self.sort(
            reverse=reverse,
            key=self._get_name_key
        )

        if locked_at_bottom:
            self._send_locked_entries_to_bottom()

        return self

    @staticmethod
    def _get_unread_key(item):
        """
        Returns:
            Key for sorting by status
        """
        return item.status
        
    def sort_by_unread(self):
        """
        Like sort_by_name, but unread entries appear at the top of the list.

        Returns:
            self
        """
        # Sort by name first
        self.sort_by_name()
                       
        self.sort(key=self._get_unread_key)
        
        # Locked entries should always be at the bottom,
        # since they can never be unread or read
        self._send_locked_entries_to_bottom()

        return self