# Copyright 2015 Joshua Fehler <jsfehler@gmail.com>
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

import copy


class EntryList(list):
    """ list that's been extended with specific sorting options """
    
    def _push_to_bottom(self, list_instance, item):
        """
        Take a list and an item in that list. 
        Pop the item from the list and insert it at the bottom.
        
        Parameters:
            list_instance: The list to use
            item: The item to push to the bottom
        
        Returns:
            The list_instance
        """
        list_length = len(list_instance)
        popped = list_instance.pop(list_instance.index(item))
        list_instance.insert(list_length, popped)
        
        return list_instance
        
    def _send_locked_entries_to_bottom(self):
        """
        Pushes all the locked entries to the bottom of the list.
        
        Used when locked entries should appear at the bottom of the list.

        Returns:
            The list
        """
        
        # We can't pop and insert directly; the loop will get screwed up.   
        changed_all_entries = copy.copy(self)

        # Loop over self.all_entries, but do the changes to changed_all_entries
        for item in self:
            if item.locked is not False:
                changed_all_entries = self._push_to_bottom(changed_all_entries, item)
        
        del self[:]
        for item in changed_all_entries:
            self.append(item)        
        
        return self

    def _get_number_key(self, item):
        return item.number
        
    def sort_by_number(self):
        return self.sort(key=self._get_number_key)        
        
    def _get_name_key(self, item):
        return item.name        
        
    def sort_by_name(self, reverse=False, locked_at_bottom=True):
        self.sort(
            reverse=reverse,
            key=self._get_name_key
        )

        if locked_at_bottom:
            self._send_locked_entries_to_bottom()
                                  
    def _get_unread_key(self, item):
        return item.status    
        
    def sort_by_unread(self):
        # Sort by name first
        self.sort_by_name()
                       
        self.sort(key=self._get_unread_key)
        
        # In this scenario, locked entries should always be at the bottom, since they can never be unread or read
        self._send_locked_entries_to_bottom()