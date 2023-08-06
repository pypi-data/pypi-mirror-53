marshallEngine 
=========================

.. image:: https://readthedocs.org/projects/marshallEngine/badge/
    :target: http://marshallEngine.readthedocs.io/en/latest/?badge
    :alt: Documentation Status

.. image:: https://cdn.rawgit.com/thespacedoctor/marshallEngine/master/coverage.svg
    :target: https://cdn.rawgit.com/thespacedoctor/marshallEngine/master/htmlcov/index.html
    :alt: Coverage Status

*A python package and command-line tools for The engine behind the marshall webapp*.





Command-Line Usage
==================

.. todo::

    - add usage

Installation
============

The easiest way to install marshallEngine is to use ``pip``:

.. code:: bash

    pip install marshallEngine

Or you can clone the `github repo <https://github.com/thespacedoctor/marshallEngine>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/marshallEngine.git
    cd marshallEngine
    python setup.py install

To upgrade to the latest version of marshallEngine use the command:

.. code:: bash

    pip install marshallEngine --upgrade


Documentation
=============

Documentation for marshallEngine is hosted by `Read the Docs <http://marshallEngine.readthedocs.org/en/stable/>`__ (last `stable version <http://marshallEngine.readthedocs.org/en/stable/>`__ and `latest version <http://marshallEngine.readthedocs.org/en/latest/>`__).

Command-Line Tutorial
=====================

Before you begin using marshallEngine you will need to populate some custom settings within the marshallEngine settings file.

To setup the default settings file at ``~/.config/marshallEngine/marshallEngine.yaml`` run the command:

.. code-block:: bash 
    
    marshallEngine init

This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an ``XXX`` placeholder). 

.. todo::

    - add tutorial

