init python:
    def persistent_status_flags(total,
                                master_key='new', status_name='new_status'):
        """Create a dictionary with specific keys in ren'py persistent and
        with None pre-filled for the values. Each item in the dictionary
        can then be used for the .viewed flag of an EncEntry.

        Should be used only if an Encyclopaedia is not tied to a saved game and
        the .viewed status of an entry should be the same across all
        saved games.

        This creates the variables, but it's up to you to use them in
        the "viewed" argument for an EncEntry.

        This function must always be called in an init python block. Due to how
        ren'py persistent works, this function will only set the dictionary the
        first time it's ever run.

        Args:
            total (int): Number of entries to create.
            master_key (str): Name of the key prefix.
                              ie: {<master_key>_01: None}
            status_name (str): Name of the persistent variable.

        Returns:
            bool: True if persistent dict created, False if not
        """
        if getattr(persistent, status_name) is None:
            # Add a number to the end of master_key
            master_key = "{}_%02d".format(master_key)
            new_status = {master_key % x: None for x in xrange(total)}

            setattr(persistent, status_name, new_status)

            return True

        return False
