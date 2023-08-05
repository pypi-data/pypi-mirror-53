cfme-testcases
==============

.. image:: https://gitlab.com/mkourim/cfme-testcases/badges/master/pipeline.svg
    :target: https://gitlab.com/mkourim/cfme-testcases/commits/master
    :alt: Pipeline status

.. image:: https://img.shields.io/pypi/v/cfme-testcases.svg
    :target: https://pypi.python.org/pypi/cfme-testcases
    :alt: Version

.. image:: https://img.shields.io/pypi/pyversions/cfme-testcases.svg
    :target: https://pypi.python.org/pypi/cfme-testcases
    :alt: Supported Python versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black


* import requirements missing in Polarion
* import test cases missing in Polarion
* update existing test cases, link missing requirements
* create new test run in Polarion or update an existing test run with newly imported test cases

All this with single command, using just the Polarion Importers. The legacy webservices API is not used at all.

Usage
-----

Run in the integration tests repository in your usual virtual environment.

.. code-block::

    cfme_testcases_upload.py -t {testrun id} -c {polarion_tools.yaml}

Install
-------

To install the package to your virtualenv, run

.. code-block::

    pip install cfme-testcases
    # or
    pip install -e .

Requirements
------------

.. code-block::

    pip install -r requirements.txt
