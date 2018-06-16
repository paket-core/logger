"""Database utils."""
import contextlib
import os

import mysql.connector

USER = os.environ['PAKET_DB_USER']
PASSWORD = os.environ['PAKET_DB_PASSWD']

@contextlib.contextmanager
def sql_connection(db_name=None, user=None, password=None):
    """Context manager for querying the database."""
    try:
        connection = mysql.connector.connect(database=db_name, user=user or USER, passwd=password or PASSWORD)
        yield connection.cursor(dictionary=True)
        connection.commit()
    except mysql.connector.Error as db_exception:
        raise db_exception
    finally:
        if 'connection' in locals():
            # noinspection PyUnboundLocalVariable
            connection.close()
