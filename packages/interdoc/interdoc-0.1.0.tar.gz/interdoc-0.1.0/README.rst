========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/interdoc/badge/?style=flat
    :target: https://readthedocs.org/projects/interdoc
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/metatooling/interdoc.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/metatooling/interdoc

.. |version| image:: https://img.shields.io/pypi/v/interdoc.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/interdoc

.. |commits-since| image:: https://img.shields.io/github/commits-since/metatooling/interdoc/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/metatooling/interdoc/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/interdoc.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/interdoc

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/interdoc.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/interdoc

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/interdoc.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/interdoc


.. end-badges

Interactive docs

* Free software: MIT License

Installation
============

::

    pip install interdoc

Documentation
=============


https://interdoc.readthedocs.io/


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
