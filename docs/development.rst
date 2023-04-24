Development
===========

Requirements: `tox`

`Tox <https://tox.readthedocs.io/en/latest/>`_ is used for managing the test environments.

Running the unit tests
----------------------

The unit tests can be run in any of the follow envs: py39

.. code-block:: console

    tox -e {env}

Running the code linter
-----------------------

.. code-block:: console

    tox -e lint


Building the distribution file
------------------------------

.. code-block:: console

    tox -e build


Building the documentation game
--------------------------------

.. code-block:: console

    tox -e build_docsgame
