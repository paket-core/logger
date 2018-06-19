"""Database utils."""
import contextlib
import functools

import mysql.connector


@contextlib.contextmanager
def sql_connection(db_name=None, host=None, port=3306, user=None, password=None):
    """Context manager for querying the database."""
    try:
        connection = mysql.connector.connect(host=host, port=port, user=user, passwd=password, database=db_name)
        yield connection.cursor(dictionary=True)
        connection.commit()
    except mysql.connector.Error as db_exception:
        raise db_exception
    finally:
        if 'connection' in locals():
            # noinspection PyUnboundLocalVariable
            connection.close()


def custom_sql_connection(host=None, port=3306, user=None, password=None, db_name=None):
    """Return a customized sql_connection context manager."""
    return functools.partial(sql_connection, db_name, host, port, user, password)
