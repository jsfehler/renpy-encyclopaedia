Changelog
=========

[3.5.0] - 2024-11-10
--------------------

Added
~~~~~

- `Encyclopaedia.set_entry()` as the non-Action equivalent to `SetEntry()`.
- Hyperlink now supports opening a Book

Fixed
~~~~~

- Any time `EncEntry.viewed` is set to True, the "viewed" callback is triggered,
  instead of only after the `SetEntry`, `NextEntry`, `PreviousEntry` Actions
  are called.

[3.4.1] - 2024-10-21
--------------------

Changed
~~~~~~~

- When trying to get the active page on an empty Book, `GetEntryError` is raised instead of `IndexError`.

Fixed
~~~~~

- Crash when using the `ChangeEntry` Action on a Book.
- When using the `SetEntry` Action on a Book, the first page was not marked as viewed.
- When using `Encyclopaedia.next_entry()` or `Encyclopaedia.previous_entry()` to reach a Book, the first page was not marked as viewed.

[3.4.0] - 2024-10-14
--------------------

Added
~~~~~

- Book object for grouping EncEntry.

Changed
~~~~~~~

- `AddEntryError` is raised when adding an entry fails, instead of ValueError.
- The attribute EncEntry.has_pages has been removed. Use `len(EncEntry().pages) > 1` instead.
- The method `Encyclopaedia.add_entry_to_unlocked_entries()` is now private and renamed to `Encyclopaedia._add_entry_to_unlocked_entries()`
- The method `EncEntry.add_entry_to_unlocked_entries()` is now private and renamed to `EncEntry._add_entry_to_unlocked_entries()`

[3.3.0] - 2024-07-21
--------------------

Added
~~~~~

- AchievementEncEntry, an EncEntry which uses achievements to manage state.

Changed
~~~~~~~

- The attribute EncEntry.label has been removed. Use `str(EncEntry)` instead.

[3.2.0] - 2024-03-10
--------------------

Added
~~~~~

- `enc_utils.text_block` function for handling large strings.

Fixed
~~~~~

- Crash when `viewed_persistent` is true and the user sorts by unread entries.

[3.1.0] - 2024-02-26
--------------------

Changed
~~~~~~~

- SetEntry Action now set selected status on buttons that use it.

- The design of the vertical list of Entries has been tweaked to use a solid
  background.

Fixed
~~~~~

- When multiple EncEntries had pages, their order was not tracked correctly.
  This is fixed in the Encyclopaedia and on the screens.

[3.0.2] - 2024-02-17
--------------------

Fixed
~~~~~

- Crash when Constants used by Actions and Encyclopaedia init after them.

[3.0.1] - 2023-11-12
--------------------

Fixed
~~~~~

- Crash while sorting when using locked_persistent.


[3.0.0] - 2023-06-13
--------------------

Added
~~~~~
- Support for hyperlinking to entries.
- CloseActiveEntry action. This will safely close the entry screen.
- Encyclopaedia.name attribute added.
- len(Encyclopaedia) returns the number of entries in the Encyclopaedia.
- Encyclopaedia.list_screen can be used to store the name of the list screen used.

Changed
~~~~~~~
- Minimum Ren'Py version bumped up to 8.1.0.
- MatrixColor is used for locked image tint instead of im.
- Encyclopaedia.set_global_locked_image_tint() method removed. Use EncEntryTemplate instead.
- Encyclopaedia.set_global_locked_name() method removed. Use EncEntryTemplate instead.
- Default screens now use Ren'Py's GUI styles.
- encyclopaedia_list screen now uses a dropdown for subject filters.
- Migrate from python 2.7 to 3.9.
- Docstrings almost entirely rewritten.
- _ren.py format used to simplify dist process.
- User Guide rewritten.
- EncEntry.add_entry raises ValueError instead of AttributeError when adding an Entry that already has a parent.

Fixed
~~~~~
- Actions now inherit from DictEquality.
