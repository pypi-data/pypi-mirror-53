

.. image:: ./assets/logo.png
   :target: ./assets/logo.png
   :alt: FlakeHell

===============================================================================


.. image:: https://badge.fury.io/py/flakehell.svg
   :target: https://badge.fury.io/py/flakehell
   :alt: PyPI version


.. image:: https://travis-ci.org/life4/flakehell.svg?branch=master
   :target: https://travis-ci.org/life4/flakehell
   :alt: Build Status


.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT


.. image:: https://readthedocs.org/projects/flakehell/badge/?version=latest
   :target: https://flakehell.readthedocs.io/
   :alt: Documentation


It's a `Flake8 <https://gitlab.com/pycqa/flake8>`_ wrapper to make it cool.


* Shareable and remote configs.
* Legacy-friendly: ability to get report only about new errors.
* Use only specified plugins, not everything installed.
* Manage codes per plugin.
* Enable and disable plugins and codes by wildcard.
* Make output beautiful.
* `pyproject.toml <https://www.python.org/dev/peps/pep-0518/>`_ support.
* Show codes for installed plugins.
* Show all messages and codes for a plugin.
* Check that all required plugins are installed.
* Syntax highlighting in messages and code snippets.
* `PyLint <https://github.com/PyCQA/pylint>`_ integration.
* Allow codes intersection for different plugins.


.. image:: ./assets/grouped.png
   :target: ./assets/grouped.png
   :alt: output example


Installation
------------

.. code-block:: bash

   python3 -m pip install --user flakehell

Usage
-----

First of all, let's create ``pyproject.toml`` config:

.. code-block::

   [tool.flakehell]
   # optionally inherit from remote config (or local if you want)
   base = "https://raw.githubusercontent.com/life4/flakehell/master/pyproject.toml"
   # specify any flake8 options. For example, exclude "example.py":
   exclude = ["example.py"]
   # make output nice
   format = "grouped"
   # 80 chars aren't enough in 21 century
   max_line_length = 90
   # show line of source code in output
   show_source = true

   # list of plugins and rules for them
   [tool.flakehell.plugins]
   # include everything in pyflakes except F401
   pyflakes = ["+*", "-F401"]
   # enable only codes from S100 to S199
   flake8-bandit = ["-*", "+S1??"]
   # enable everything that starts from `flake8-`
   "flake8-*" = ["+*"]
   # explicitly disable plugin
   flake8-docstrings = ["-*"]

Show plugins that aren't installed yet:

.. code-block:: bash

   flakehell missed

Show installed plugins, used plugins, specified rules, codes prefixes:

.. code-block:: bash

   flakehell plugins


.. image:: ./assets/plugins.png
   :target: ./assets/plugins.png
   :alt: plugins command output


Show codes and messages for a specific plugin:

.. code-block:: bash

   flakehell codes pyflakes


.. image:: ./assets/codes.png
   :target: ./assets/codes.png
   :alt: codes command output


Run flake8 against the code:

.. code-block:: bash

   flakehell lint

This command accepts all the same arguments as Flake8.

Read `flakehell.readthedocs.io <https://flakehell.readthedocs.io/>`_ for more information.


.. image:: ./assets/flaky.png
   :target: ./assets/flaky.png
   :alt: 


The FlakeHell mascot (Flaky) is created by `@diana_leit <https://www.instagram.com/diana_leit/>`_ and licensed under the `CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_ license.
