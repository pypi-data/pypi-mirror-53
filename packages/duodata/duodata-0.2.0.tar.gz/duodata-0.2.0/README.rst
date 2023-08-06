========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-duodata/badge/?style=flat
    :target: https://readthedocs.org/projects/python-duodata
    :alt: Documentation Status


.. |version| image:: https://img.shields.io/pypi/v/duodata.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/duodata

.. |commits-since| image:: https://img.shields.io/github/commits-since/enningb/python-duodata/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/enningb/python-duodata/compare/v0.2.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/duodata.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/duodata

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/duodata.svg
    :alt: Supported versions
    :target: https://pypi.org/project/duodata

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/duodata.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/duodata


.. end-badges

A package that extracts data from Dienst Uitvoering Onderwijs.

* Free software: MIT license

Installation
============

::

    pip install duodata

Documentation
=============


https://python-duodata.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
