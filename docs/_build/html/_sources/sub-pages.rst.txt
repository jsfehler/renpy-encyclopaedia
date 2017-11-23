Sub-Pages
=========

Just like an Encyclopaedia holds EncEntry objects, each EncEntry can hold other EncEntry objects.
This allows entries to be paginated.

EncEntry objects that are used as sub-pages are created the same way as other EncEntry,
but instead of providing an Encyclopaedia as the parent, the first EncEntry page is used.

When adding sub-pages, the parent EncEntry is considered the first page in the entry. Added sub-pages are numbered starting from 2.
