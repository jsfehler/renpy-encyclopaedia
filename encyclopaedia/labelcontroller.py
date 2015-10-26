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

from math import floor


class LabelController(object):
    """
    Controls how the labels that display Encyclopaedia data appear.
    """
    def __init__(self, encyclopaedia):
        self.encyclopaedia = encyclopaedia
   
        # Placed next to the percentage unlocked number
        self.percentage_label = '%'
        
        # Placed before the entry page displayed
        self.page_label = 'Page'
        
        # Placed in-between the current page number and the total page number 
        self.page_separator_label = '/'
   
        # Variables for the strings representing the different sorting types
        self.sort_number_label = "Number"
        self.sort_alphabetically_label = "A to Z"
        self.sort_reverse_alphabetically_label = "Z to A"
        self.sort_subject_label = "Subject"
        self.sort_unread_label = "Unread"

    @property
    def percentage_unlocked(self): 
        """ 
        Returns: 
            String displaying the percentage of the encyclopaedia
            that's unlocked, ie: '50%'
        """
        
        float_size = float(self.encyclopaedia._size)
        float_size_all = float(self.encyclopaedia._size_all)
        
        amount_unlocked = float_size / float_size_all
        percentage = floor(amount_unlocked * 100)
        label = str(int(percentage)) + self.percentage_label 
        
        return label   

    @property
    def entry_current_page(self):
        """
        Returns: 
            String indicating which sub-page of an entry is being viewed
        """
        label = "%s %d %s %d" % (
            self.page_label, 
            self.encyclopaedia.sub_current_position, 
            self.page_separator_label, 
            self.encyclopaedia.active.pages
        ) 
        
        return label
     
    @property
    def sorting_mode(self):
        """
        Returns:
            String representation of the current sorting mode
        """

        enc = self.encyclopaedia

        sorting_strings = {
            enc.SORT_NUMBER: self.sort_number_label,
            enc.SORT_ALPHABETICALLY: self.sort_alphabetically_label,
            enc.SORT_REVERSE_ALPHABETICALLY: self.sort_reverse_alphabetically_label,
            enc.SORT_SUBJECT: self.sort_subject_label,
            enc.SORT_UNREAD: self.sort_unread_label
        }

        return sorting_strings[enc.sorting_mode]