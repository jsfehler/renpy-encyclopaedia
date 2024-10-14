.. _sub_pages:

Sub-Pages
=========

.. note::
  As of version 3.4.0, the :ref:`Book <migration_to_book>`  object is available.
  A Book can do everything Sub-Pages can and more.

Just like an Encyclopaedia holds EncEntry objects, each EncEntry can hold other EncEntry objects.
This allows entries to be paginated.

EncEntry which are used as sub-pages are created the same way as any other EncEntry,
but instead of providing an Encyclopaedia as the parent, an EncEntry is used.

When adding sub-pages, the parent EncEntry is considered the first page in the entry.
Added sub-pages are numbered starting from 2.
