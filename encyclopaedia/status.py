from ast import literal_eval

import renpy.exports as renpy

persistent = renpy.game.persistent


class StatusFlagGenerator(object):

    @staticmethod
    def __make_persistent_dict(total, master_key, persistent_var_string):
        """
        For the total amount given,
            1) takes two strings to define a series of keys and values in a
                dictionary.
            2) Creates two lists and evaluates the values to variables.
            3) Then combines the lists into a dictionary.

        Parameters:
            total: The number of entries in the dictionary that's going to
                be made.
            master_key: The prefix for the keys
            persistent_var_string: The string that will be turned into the
                variables for the values in the dictionary

        Returns:
            Dictionary with persistent values
        """

        # eg: [new_00, new_01, etc]
        keys = [master_key % x for x in range(total)]

        # eg:
        # "persistent.new_status["new_00"]",
        # "persistent.new_status["new_01"]", etc
        value_str = [persistent_var_string % x for x in range(total)]
        # Eval strings into the actual variables
        values = [eval(item) for item in value_str]
        combo = zip(keys, values)
        return dict(combo)

    @classmethod
    def create_persistent_status_flags(
            cls,
            total=0,
            master_key='new',
            name="new"):
        """
        Create the persistent status variables to manage the "New!" status if
        the Encyclopaedia is save game independent.

        If the Encyclopaedia is tied to a save game state, using persistent
        variables is unnecessary.

        This will create the variables, but it's up to you to use them in
        the "status" argument for an EncEntry.

        This function must always be called when the game starts.

        If you want a save game specific "New!" status,
        don't use persistent variables,
        and create the EncEntry after the start label, not in an init block.

        How it works:
        Two dictionaries are created:
        persistent.<name>_cache
        persistent.<name>_dict.

        master_key is the prefix for all the keys in both dictionaries.
        name is the prefix for the dictionary names.
        Both default to "new".

        When this function runs, each key in persistent.new_cache is
        given the value of an entry in persistent.new_status and vice versa.
        eg: persistent.new_cache["new_00"] = persistent.new_status["new_00"]
            persistent.new_status["new_00"] = persistent.new_status["new_00"]

        Each EncEntry must use persistent.new_status["new_<x>"]
        for their status variable.
        <x> being an integer.

        Why it works:
        If the value is None or False, "New!" is displayed.
        As each entry is opened and exited, the value in new_status
        is set to True.

        Each time the game is started, new_cache is set to
        whatever the matching new_status value is.
        new_status then sets itself to whatever new_cache is.

        The reason this is all necessary is that if an Encyclopaedia
        is created in an init block, there's no way to save the data without
        using persistent data, but you don't want the init to reset
        the persistent data each time the game opens and the Encyclopaedia is
        created anew.
        """

        # Build strings that represent the persistent dictionaries.
        # ie: "persistent.new_cache" and "persistent.new_status"
        master_key += "_0%s"
        persistent_str = 'persistent.'

        status_name = name + "_status"
        cache_name = name + "_cache"

        try:
            # Create a dictionary with the following key/value pairs:
            # 'new_01': persistent.new_<dict_name>['new_01']
            dict_of_keys = cls.__make_persistent_dict(
                total,
                master_key,
                '%s%s["%s"]' % (persistent_str, status_name, master_key)
            )

        except (TypeError, KeyError) as e:
            # The first time the Encyclopaedia is launched,
            # persistent.new_<dict_name> doesn't exist yet, causing a TypeError.

            # In development, the dictionary may already exist,
            # but without the correct number of keys, causing a KeyError.

            # Create a dictionary with the following key/value pairs:
            # 'new_01': None
            dict_of_keys = {master_key % k: None for k in range(total)}

        # Populate cache of status variables
        setattr(
            persistent,
            cache_name,
            dict_of_keys
        )

        # Create a dictionary with the following key/value pairs:
        # 'new_01': persistent.new_<cache_name>['new_01']
        dict_of_values = cls.__make_persistent_dict(
            total,
            master_key,
            '%s%s["%s"]' % (persistent_str, cache_name, master_key)
        )

        # Populate status variables with cache values
        setattr(
            persistent,
            status_name,
            dict_of_values
        )