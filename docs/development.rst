Development
===========

Requirements:

    - Python 3.9
    - `Tox <https://tox.readthedocs.io/en/latest/>`_


Run the unit tests
------------------

.. code-block:: console

    tox -e tests


Run the code linter
-------------------

.. code-block:: console

    tox -e lint


Build the distribution file
---------------------------

.. code-block:: console

    tox -e build


Build the documentation
-----------------------

Create a static copy of the documentation in HTML format.

.. code-block:: console

    tox -e build_docs_html


Build the documentation game
----------------------------

.. code-block:: console

    tox -e build_docsgame
