"""Database utils."""
import contextlib
import sqlite3


@contextlib.contextmanager
def sql_connection(db_name):
    """Context manager for querying the database."""
    try:
        connection = sqlite3.connect(db_name)
        connection.row_factory = sqlite3.Row
        yield connection.cursor()
        connection.commit()
    except sqlite3.Error as db_exception:
        raise db_exception
    finally:
        if 'connection' in locals():
            # noinspection PyUnboundLocalVariable
            connection.close()
