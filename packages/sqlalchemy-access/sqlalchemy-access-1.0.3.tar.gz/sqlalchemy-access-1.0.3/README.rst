sqlalchemy-access
=================

A Microsoft Access dialect for SQLAlchemy.

Objectives
----------

This dialect is mainly intended to offer
pandas users an easy way to save a DataFrame into an
Access database via ``to_sql``.

Pre-requisites
--------------

- If you already have Microsoft Office (or standalone Microsoft Access) installed then install a version
  of Python with the same "bitness". For example, if you have 32-bit Office then you should install
  32-bit Python.

- If you do not already have Microsoft Office (or standalone Microsoft Access) installed then install
  the version of the Microsoft Access Database Engine Redistributable with the same "bitness" as the
  version of Python you will be using. For example, if you will be running 64-bit Python then you
  should install the 64-bit version of the Access Database Engine.

Special case: If you will be running 32-bit Python and you will **only** be working with .mdb files
then you can use the older 32-bit ``Microsoft Access Driver (*.mdb)`` that ships with Windows.

Co-requisites
-------------

This dialect requires SQLAlchemy and pyodbc. They are both specified as requirements so ``pip`` will install
them if they are not already in place. To install, just::

    pip install sqlalchemy-access

Getting Started
---------------

Create an `ODBC DSN (Data Source Name)`_ that points to your Access database.
(Tip: For best results, enable `ExtendedAnsiSQL`_.)
Then, in your Python app, you can connect to the database via::

    from sqlalchemy import create_engine
    engine = create_engine("access+pyodbc://@your_dsn")

For other ways of connecting see the `Getting Connected`_ page in the Wiki.

.. _ODBC DSN (Data Source Name): https://support.microsoft.com/en-ca/help/966849/what-is-a-dsn-data-source-name
.. _ExtendedAnsiSQL: https://github.com/sqlalchemy/sqlalchemy-access/wiki/%5Btip%5D-use-ExtendedAnsiSQL
.. _Getting Connected: https://github.com/sqlalchemy/sqlalchemy-access/wiki/Getting-Connected