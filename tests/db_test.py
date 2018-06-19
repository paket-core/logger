"""Tests for db module"""
import os
import unittest

import util.db
import util.logger


DB_HOST = os.environ.get('PAKET_DB_HOST', '127.0.0.1')
DB_PORT = int(os.environ.get('PAKET_DB_PORT', 3306))
DB_USER = os.environ.get('PAKET_DB_USER', 'root')
DB_PASSWORD = os.environ.get('PAKET_DB_PASSWORD')
DB_PASSWORD = os.environ.get('PAKET_DB_PASSWORD')
DB_NAME = 'paket_test'
LOGGER = util.logger.logging.getLogger('pkt.util.test')
util.logger.setup()


class TestDB(unittest.TestCase):
    """Tests for db"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql = util.db.custom_sql_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    def setUp(self):
        LOGGER.info('setting up')
        with self.sql() as sql:
            sql.execute("DROP DATABASE IF EXISTS {}".format(DB_NAME))
            sql.execute("CREATE DATABASE {}".format(DB_NAME))

    def test_sql(self):
        """Test selecting from just created and filled table"""
        LOGGER.info('creating and filling new table')
        with self.sql() as sql:
            sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')
            sql.execute('INSERT INTO test (id, number) VALUES (0, 144)')
            sql.execute('INSERT INTO test (id, number) VALUES (1, 13)')
            sql.execute('INSERT INTO test (id, number) VALUES (2, 37)')
        LOGGER.info('selecting data from table')
        with self.sql() as sql:
            sql.execute('SELECT number FROM test WHERE number > 100')
            result = sql.fetchall()
            self.assertNotEqual(result, None)
            self.assertEqual(result[0]['number'], 144)

    def test_closing(self):
        """Test closing connection"""
        LOGGER.info('creating new table')
        with self.sql() as sql:
            sql.execute('DROP TABLE IF EXISTS test')
            sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')
        LOGGER.info('attempting operation after closing connection')
        with self.assertRaises(ReferenceError):
            sql.fetchone()

    def test_closing_on_exception(self):
        """Test closing connection on exception"""
        # YARIK, why doesn't this use self.assertRaises?
        LOGGER.info('expecting raising exception')
        try:
            with self.sql() as sql:
                sql.execute('DROP TABLE IF EXISTS test;')
                sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')
                sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')  # should raise ProgrammingError
        # pylint: disable=broad-except
        except Exception:
            pass  # ignore raised Exception
        # pylint: enable=broad-except
        finally:
            LOGGER.info('attempting operation after raising exception')
            with self.assertRaises(ReferenceError):
                sql.fetchone()
