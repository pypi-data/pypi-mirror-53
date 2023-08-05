========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-melthon/badge/?style=flat
    :target: https://readthedocs.org/projects/python-melthon
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/jenswbe/python-melthon.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jenswbe/python-melthon

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jenswbe/python-melthon?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jenswbe/python-melthon

.. |requires| image:: https://requires.io/github/JenswBE/python-melthon/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/JenswBE/python-melthon/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/melthon.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/melthon

.. |commits-since| image:: https://img.shields.io/github/commits-since/jenswbe/python-melthon/v1.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jenswbe/python-melthon/compare/v1.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/melthon.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/melthon

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/melthon.svg
    :alt: Supported versions
    :target: https://pypi.org/project/melthon

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/melthon.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/melthon


.. end-badges

Minimalistic static site generator

* Free software: GNU GPLv3 license

Installation
============

::

    pip install melthon

Documentation
=============


https://python-melthon.readthedocs.io/


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
