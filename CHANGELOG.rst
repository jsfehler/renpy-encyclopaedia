Changelog
=========

[3.0.0] - 2023-05-23
--------------------

Added
~~~~~
- Support for hyperlinking to entries.
- CloseActiveEntry action. This will safely close the entry screen.
- Encyclopaedia.name attribute added.

Changed
~~~~~~~
- Minimum Ren'Py version bumped up to 8.1.0
- MatrixColor is used for locked image tint instead of im
- Encyclopaedia.set_global_locked_image_tint() method removed. Use EncEntryTemplate instead.
- Encyclopaeda.set_global_locked_name() method removed. Use EncEntryTemplate instead.
- Default screens now use Ren'Py's GUI styles
- Migrate from python 2.7 to 3.9
- Docstrings almost entirely rewritten
- _ren.py format used to simplify dist process
- User Guide rewritten

Fixed
~~~~~
- Actions now inherit from DictEquality
