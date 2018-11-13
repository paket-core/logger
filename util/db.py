"""Database utils."""
import contextlib
import functools
import re

import mysql.connector


class DataTooBig(Exception):
    """Data too big for database column."""


@contextlib.contextmanager
def sql_connection(db_name=None, host=None, port=3306, user=None, password=None):
    """Context manager for querying the database."""
    try:
        connection = mysql.connector.connect(host=host, port=port, user=user, passwd=password, database=db_name)
        yield connection.cursor(dictionary=True)
        connection.commit()
    except mysql.connector.DataError as data_error:
        check_data_error(data_error)
    except mysql.connector.Error as db_error:
        raise db_error
    finally:
        if 'connection' in locals():
            # noinspection PyUnboundLocalVariable
            connection.close()


def check_data_error(data_error):
    """Check if data error is caused by size of inserted data."""
    error_message = str(data_error)
    if 'Out of range value' in error_message or 'Data too long' in error_message:
        column_name = re.search('^.+\'(.+)\'.+', error_message).group(1)
        raise DataTooBig("Data too big for {}".format(column_name))

    raise data_error


def custom_sql_connection(host=None, port=3306, user=None, password=None, db_name=None):
    """Return a customized sql_connection context manager."""
    return functools.partial(sql_connection, db_name, host, port, user, password)


def clear_tables(active_sql_connection, db_name):
    """Clear all tables in the database."""
    with active_sql_connection() as sql:
        sql.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = %s", (db_name,))
        for table_name in [row['TABLE_NAME'] for row in sql.fetchall()]:
            sql.execute("DELETE from {}".format(table_name))


def drop_tables(active_sql_connection, db_name):
    """Drop all tables in the database."""
    with active_sql_connection() as sql:
        sql.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = %s", (db_name,))
        for table_name in [row['TABLE_NAME'] for row in sql.fetchall()]:
            sql.execute("DROP TABLE {}".format(table_name))


def get_table_columns(active_sql_connection, db_name, table_name):
    """Get the fields of a specific table."""
    with active_sql_connection() as sql:
        sql.execute("""
            SELECT TABLE_NAME FROM information_schema.tables
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s""", (db_name, table_name))
        tables = sql.fetchall()
        assert len(tables) == 1, "table {} does not exist".format(table_name)
        sql.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                    (db_name, table_name))
        return [column['COLUMN_NAME'] for column in sql.fetchall()]
