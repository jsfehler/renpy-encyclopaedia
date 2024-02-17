Installation
============

Using Pip
---------

As of version `3.0` the renpy-encyclopaedia project can be installed using `pip <https://pip.pypa.io/en/stable/>`_.

.. warning::
  Although it uses many parts of the Python ecosystem,
  renpy-encyclopaedia is **not** a stand-alone python package and is not designed to work outside
  of a Ren'Py project.

From the console, navigate into your project's directory and run the following command:

.. code-block:: console

    pip install --no-compile --target game git+https://github.com/jsfehler/renpy-encyclopaedia.git@3.0.1#egg=renpy-encyclopaedia

The target directory can be anywhere inside `game/`. Ren'Py is able to detect any valid code inside your project.

Manual
------

1. Download the latest release at: https://github.com/jsfehler/renpy-encyclopaedia/releases
2. Place the `encyclopaedia` folder inside your project's `game` directory.

Compatibility With Ren'Py
-------------------------

Version 2.x of the Encyclopaedia is compatible with ``Ren'Py 6.99.12.3`` and up.

Version 3.x of the Encyclopaedia is compatible with ``Ren'Py 8.1.0`` and up.

Generally, you should use the latest version of the Encyclopaedia with the latest
version of Ren'Py. Version 2 of the Encyclopaedia is no longer developed and
only useful for games that are stuck on older versions of Ren'py.
