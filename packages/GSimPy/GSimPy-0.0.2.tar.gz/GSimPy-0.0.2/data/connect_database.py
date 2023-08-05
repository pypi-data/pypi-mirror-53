"""
.. note::
    This module provides methods to let users connect to the specific database


"""

import sqlite3


def connect_database(database_name):
    """
       It provides interface for users to connect to the specific database.
       If a database dose not exist, a database is automatically created.

    :param database_name: string
            The database that connect to
    :return: conn
             sqlite3.Connection, link to the database in sqlite
    """
    # conn = sqlite3.connect('C:/Users/张逸飞/PycharmProjects/R-DGS1.0.2/{}.db'.format(database_name))
    # conn = sqlite3.connect('../data/{}.db'.format(database_name))
    # print('open database successfully')

    conn = sqlite3.connect(database_name)

    return conn


# connect_database('sample')