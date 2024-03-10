Tools
=====

Although the Encyclopaedia framework is designed as a plugin for Ren'Py, it's
written almost entirely in Python. Consequently, it uses the Python
ecosystem for development and testing.

The framework's Python version matches Ren'Py's, thus `3.9` must be installed
to build and test the plugin. The following Python libraries must be installed as well:

  - `Tox <https://tox.readthedocs.io/en/latest/>`_

Setting up python on your machine and installing dependencies are beyond the
scope of the plugin's documentation.

Run the unit tests
------------------

.. code-block:: console

    tox -e tests


Run the code linter
-------------------

.. code-block:: console

    tox -e lint


Build the documentation
-----------------------

Create a static copy of the documentation in HTML format.

.. code-block:: console

    tox -e build_docs_html


Build the documentation game
----------------------------

.. code-block:: console

    tox -e build_docsgame
