init python:
    def persistent_status_flags(total,
                                master_key='new', status_name='new_status'):
        """Create a dictionary in ren'py persistent with None pre-filled for
        the values.

        Used only if an Encyclopaedia is not tied to a save game state and
        should unlock entries across all save games.

        This creates the variables, but it's up to you to use them in
        the "viewed" argument for an EncEntry.

        This function must always be called in an init python block.

        Args:
            total (int): Number of entries to create.
            master_key (str): Name of the key prefix.
                              ie: {<master_key>_01: None}
            status_name (str): Name of the persistent variable.

        Returns:
            bool: True if persistent dict created, False if not
        """
        # If the dict for the status variables doesn't exist yet, create it.
        if getattr(persistent, status_name) is None:

            # Add a number to the end of master_key
            master_key += "_%02d"

            new_status = {master_key % x: None for x in xrange(total)}

            setattr(persistent, status_name, new_status)

            return True

        return False
