"""Database utils."""
import contextlib

import mysql.connector


@contextlib.contextmanager
def sql_connection(db_name):
    """Context manager for querying the database."""
    try:
        connection = mysql.connector.connect(database=db_name)
        yield connection.cursor()
        connection.commit()
    except mysql.connector.Error as db_exception:
        raise db_exception
    finally:
        if 'connection' in locals():
            # noinspection PyUnboundLocalVariable
            connection.close()
