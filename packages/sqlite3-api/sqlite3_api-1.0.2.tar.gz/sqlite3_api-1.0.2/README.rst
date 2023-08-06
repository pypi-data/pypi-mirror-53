Installation
------------

Install from `PyPI <https://pypi.org/project/sqlite3-api>`_::

    pip install chardet


Create table classes
--------------------

In file tables.py in the package folder, there is an instruction to create classes(in Russian language)

Using
------------

Import package::

    import sqlite3_api

Initiate the database::

    sql = sqlite3_api.API('file_name.db')

Create tables::

    sql.create_db()

Getting data::

    table_name = 'test_table'
    data = sql.filter(table_name)

Sorting data::

    table_name = 'test_table'
    data = sql.filter(table_name, field_name='value')


More information in the test folder in the package folder
VK: `AlexDev <https://vk.com/sys.exit1>`_
