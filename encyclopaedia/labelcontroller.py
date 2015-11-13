from encexceptions import NoEntryOpenError


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
        self.sort_alphabetical_label = "A to Z"
        self.sort_reverse_alphabetical_label = "Z to A"
        self.sort_subject_label = "Subject"
        self.sort_unread_label = "Unread"

        # String for an "Unread Entry" button
        self.unread_entry_label = "New!"

        # String for a "Locked Entry" button
        self.locked_entry_label = "???"

    @property
    def percentage_unlocked(self): 
        """ 
        Returns: 
            String displaying the percentage of the encyclopaedia
            that's unlocked, ie: '50%'
        """
        percentage_unlocked = self.encyclopaedia.percentage_unlocked
        label = str(int(percentage_unlocked)) + self.percentage_label
        
        return label   

    @property
    def entry_current_page(self):
        """
        Returns: 
            str: The sub-page of an entry that is being viewed
        """
        try:
            total_pages = self.encyclopaedia.active.pages
        except AttributeError:
            raise NoEntryOpenError(
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
    def sorting_mode(self):
        """
        Returns:
            str: The current sorting mode
        """
        enc = self.encyclopaedia

        sorting_strings = {
            enc.SORT_NUMBER: self.sort_number_label,
            enc.SORT_ALPHABETICAL: self.sort_alphabetical_label,
            enc.SORT_REVERSE_ALPHABETICAL: self.sort_reverse_alphabetical_label,
            enc.SORT_SUBJECT: self.sort_subject_label,
            enc.SORT_UNREAD: self.sort_unread_label
        }

        return sorting_strings[enc.sorting_mode]