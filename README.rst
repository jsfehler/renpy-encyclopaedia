Encyclopaedia Framework for Ren'Py
==================================

.. image:: https://github.com/jsfehler/renpy-encyclopaedia/workflows/CI/badge.svg
    :target: https://github.com/jsfehler/renpy-encyclopaedia/actions/workflows/test.yml
    :alt: Build status

.. image:: https://coveralls.io/repos/github/jsfehler/renpy-encyclopaedia/badge.svg?branch=master
    :target: https://coveralls.io/github/jsfehler/renpy-encyclopaedia?branch=master

A plugin for the `Ren'py Visual Novel engine <https://www.renpy.org/>`_

Simplifies creating an encyclopaedia, bestiary, glossary, or similar system.

Compatible Ren'Py Version: 6.99.12.3 and higher


Documentation
-------------
Documentation is available at http://renpy-encyclopaedia.readthedocs.io/en/latest/index.html.

Development
-----------
Requirements: `tox`

`Tox <https://tox.readthedocs.io/en/latest/>`_ is used for managing the test environments.

Running the unit tests
~~~~~~~~~~~~~~~~~~~~~~

The unit tests can be run in any of the follow envs: py27, py36, py37


.. code-block:: console

    tox -e {env}

Running the code linter
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    tox -e flake8


Building the distribution file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    tox -e build
