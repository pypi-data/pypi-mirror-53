PyBEL-CX |build| |coverage| |documentation|
===========================================
A PyBEL extension for interconversion with CX.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
PyBEL-CX can be installed easily from `PyPI <https://pypi.python.org/pypi/pybel-cx>`_ with the following code in
your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install pybel-cx

or from the latest code on `GitHub <https://github.com/pybel/pybel-cx>`_ with:

.. code-block:: sh

   $ python3 -m pip install git+https://github.com/pybel/pybel-cx.git

Command Line Usage
------------------
PyBEL-CX installs two command line utilities: ``bel_to_cx`` and ``cx_to_bel``.

CX to BEL
~~~~~~~~~
Running this script has the caveat that the CX document should conform to the schema created by PyBEL-CX.

.. code-block:: sh

   $ cat my_network.cx | cx_to_bel > my_network.bel

BEL to CX
~~~~~~~~~
.. code-block:: sh

   $ cat my_network.bel | bel_to_cx > my_network.cx

Since this operation can be expensive, PyBEL caches namespace resources. The ``-c`` flag can be used to specify a
database connection string to use a high performance RDBMS instead of the default SQLite. For example, if you would
like to use MySQL, this database string will look something like
``mysql+pymysql://<username>:<password>@<host>/<dbname>?charset=utf8[&<options>]``. Be sure to ``pip install`` the
connector, which is ``pymysql`` in this example.

.. code-block:: sh

   $ pip install pymysql
   $ cat my_network.bel | bel_to_cx -c "mysql+pymysql://root:root@localhost/mydb?charset=utf8" > my_network.cx

More documentation on connection strings at http://pybel.readthedocs.io/en/latest/manager.html#pybel.manager.BaseManager.from_connection.

.. |build| image:: https://travis-ci.com/pybel/pybel-cx.svg?branch=master
    :target: https://travis-ci.com/pybel/pybel-cx
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/pybel/pybel-cx/coverage.svg?branch=master
    :target: https://codecov.io/gh/pybel/pybel-cx?branch=master
    :alt: Coverage Status

.. |documentation| image:: http://readthedocs.org/projects/pybel-cx/badge/?version=latest
    :target: https://pybel.readthedocs.io/projects/cx/en/latest/?badge=latest
    :alt: Documentation Status

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/pybel-cx.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/pybel-cx.svg
    :alt: Current version on PyPI

.. |pypi_license| image:: https://img.shields.io/pypi/l/pybel-cx.svg
    :alt: MIT License
